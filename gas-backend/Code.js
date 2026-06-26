/**
 * Google Apps Script Web App Backend
 * Serves as the serverless API and Database Engine for the Portfolio & Referral Exchange Platform
 * Database stored in Google Sheets.
 */

// Configuration - Store this in Script Properties or edit directly here
const SPREADSHEET_ID_PROPERTY = 'SPREADSHEET_ID';

/**
 * Main GET request routing
 */
function doGet(e) {
  const params = e.parameter;
  const action = params.action;
  
  let result = { success: false, error: 'Invalid action' };
  
  try {
    const db = getDatabase();
    
    if (action === 'getMetrics') {
      result = handleGetMetrics(db);
    } else if (action === 'getReferrals') {
      result = handleGetReferrals(db);
    } else if (action === 'getSureShotJobs') {
      result = handleGetSureShotJobs(db);
    } else {
      result = { success: true, message: 'Google Apps Script Backend API Online' };
    }
  } catch (err) {
    result = { success: false, error: err.toString() };
  }
  
  return ContentService.createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Main POST request routing
 */
function doPost(e) {
  let result = { success: false, error: 'Invalid POST body or action' };
  
  try {
    let postData;
    if (e.postData && e.postData.contents) {
      postData = JSON.parse(e.postData.contents);
    } else {
      postData = e.parameter;
    }
    
    const action = postData.action;
    const db = getDatabase();
    
    if (action === 'registerHM') {
      result = handleRegisterHM(db, postData);
    } else if (action === 'postSureShotJob') {
      result = handlePostSureShotJob(db, postData);
    } else if (action === 'applySureShot') {
      result = handleApplySureShot(db, postData);
    } else if (action === 'subscribeNewsletter') {
      result = handleSubscribeNewsletter(db, postData);
    } else if (action === 'submitContact') {
      result = handleSubmitContact(db, postData);
    } else if (action === 'submitReferralUTR') {
      result = handleSubmitReferralUTR(db, postData);
    } else if (action === 'adminUpdateData') {
      result = handleAdminUpdateData(db, postData);
    } else if (action === 'adminGetSheetData') {
      result = handleAdminGetSheetData(db, postData);
    }
  } catch (err) {
    result = { success: false, error: err.toString() };
  }
  
  // Set CORS headers by returning JSON
  return ContentService.createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Database Spreadsheet getter
 */
function getDatabase() {
  const scriptProperties = PropertiesService.getScriptProperties();
  let spreadsheetId = scriptProperties.getProperty(SPREADSHEET_ID_PROPERTY);
  
  let ss;
  if (spreadsheetId) {
    try {
      ss = SpreadsheetApp.openById(spreadsheetId);
    } catch (e) {
      // ID invalid or no access
    }
  }
  
  if (!ss) {
    // If not configured, look for active spreadsheet or create a new one
    try {
      ss = SpreadsheetApp.getActiveSpreadsheet();
    } catch (e) {
      ss = SpreadsheetApp.create('Referral_Exchange_Platform_DB');
      PropertiesService.getScriptProperties().setProperty(SPREADSHEET_ID_PROPERTY, ss.getId());
    }
  }
  
  return ss;
}

/**
 * Helper to get sheet or create it with headers if missing
 */
function getOrCreateSheet(ss, name, headers) {
  let sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    if (headers && headers.length > 0) {
      sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
      sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
    }
  }
  return sheet;
}

/**
 * Get core metrics for admin dashboard
 */
function handleGetMetrics(ss) {
  const seekersSheet = getOrCreateSheet(ss, 'Seeker_Preferences', ['seeker_id', 'seeker_name', 'desired_roles', 'desired_companies', 'resume_url', 'linkedin_url', 'status']);
  const giversSheet = getOrCreateSheet(ss, 'Giver_Directory', ['id', 'name', 'company', 'linkedin_url', 'contact_email', 'status']);
  const jobsSheet = getOrCreateSheet(ss, 'Job_Inventory', ['job_id', 'seeker_id', 'company', 'title', 'link', 'date_scraped', 'status']);
  const requestsSheet = getOrCreateSheet(ss, 'Seeker_Requests', ['request_id', 'seeker_id', 'job_id', 'giver_id', 'transaction_id', 'payment_status', 'match_status']);
  
  const totalSeekers = Math.max(0, seekersSheet.getLastRow() - 1);
  const totalGivers = Math.max(0, giversSheet.getLastRow() - 1);
  const totalJobs = Math.max(0, jobsSheet.getLastRow() - 1);
  const totalRequests = Math.max(0, requestsSheet.getLastRow() - 1);
  
  return {
    success: true,
    data: {
      seekersCount: totalSeekers,
      giversCount: totalGivers,
      jobsCount: totalJobs,
      requestsCount: totalRequests,
      systemStatus: 'Healthy'
    }
  };
}

/**
 * Get public list of referrals/matches
 */
function handleGetReferrals(ss) {
  const sheet = getOrCreateSheet(ss, 'Seeker_Requests', ['request_id', 'seeker_id', 'job_id', 'giver_id', 'transaction_id', 'payment_status', 'match_status']);
  const giversSheet = getOrCreateSheet(ss, 'Giver_Directory', ['id', 'name', 'company']);
  
  const requestsData = sheet.getDataRange().getValues();
  const giversData = giversSheet.getDataRange().getValues();
  
  // Map giver names for company info
  const giverMap = {};
  for (let i = 1; i < giversData.length; i++) {
    giverMap[giversData[i][0]] = { name: giversData[i][1], company: giversData[i][2] };
  }
  
  const list = [];
  for (let i = 1; i < requestsData.length; i++) {
    const giverId = requestsData[i][3];
    const company = giverMap[giverId] ? giverMap[giverId].company : 'J.P. Morgan';
    list.push({
      id: requestsData[i][0],
      company: company,
      status: requestsData[i][6] || 'Pending',
      seeker: 'Anonymous'
    });
  }
  
  // Fallbacks if empty
  if (list.length === 0) {
    list.push(
      { id: 1, company: 'OSTTRA', status: 'Connected', seeker: 'Anonymous' },
      { id: 2, company: 'J.P. Morgan', status: 'Pending', seeker: 'Anonymous' }
    );
  }
  
  return { success: true, data: list };
}

/**
 * Get active Direct/Sure Shot Job Postings
 */
function handleGetSureShotJobs(ss) {
  const sheet = getOrCreateSheet(ss, 'Direct_Postings', ['job_id', 'manager_id', 'title', 'company', 'description', 'eligibility_criteria', 'custom_fee', 'guarantee_terms', 'date_posted', 'status']);
  const data = sheet.getDataRange().getValues();
  
  const list = [];
  for (let i = 1; i < data.length; i++) {
    if (data[i][9] === 'Active') {
      list.push({
        id: data[i][0],
        title: data[i][2],
        company: data[i][3],
        description: data[i][4],
        criteria: data[i][5],
        fee: data[i][6],
        guarantee: data[i][7],
        date: data[i][8]
      });
    }
  }
  
  return { success: true, data: list };
}

/**
 * Register Hiring Manager
 */
function handleRegisterHM(ss, data) {
  const sheet = getOrCreateSheet(ss, 'Hiring_Managers', ['manager_id', 'name', 'company', 'linkedin_url', 'corporate_email', 'status']);
  const id = 'HM_' + new Date().getTime();
  
  sheet.appendRow([
    id,
    data.name,
    data.company,
    data.linkedin || '',
    data.email,
    'Verified'
  ]);
  
  return {
    success: true,
    data: {
      managerId: id,
      name: data.name,
      company: data.company,
      email: data.email
    }
  };
}

/**
 * Post a new Sure Shot Job
 */
function handlePostSureShotJob(ss, data) {
  const sheet = getOrCreateSheet(ss, 'Direct_Postings', ['job_id', 'manager_id', 'title', 'company', 'description', 'eligibility_criteria', 'custom_fee', 'guarantee_terms', 'date_posted', 'status']);
  const id = 'JOB_' + new Date().getTime();
  
  sheet.appendRow([
    id,
    data.managerId || 'HM_SYSTEM',
    data.title,
    data.company || 'Unknown',
    data.description,
    data.criteria,
    data.fee,
    data.guarantee,
    new Date().toLocaleDateString(),
    'Active'
  ]);
  
  return { success: true, jobId: id };
}

/**
 * Apply for a Sure Shot Job
 */
function handleApplySureShot(ss, data) {
  const sheet = getOrCreateSheet(ss, 'Sure_Shot_Applications', ['application_id', 'seeker_id', 'job_id', 'portfolio_url', 'payment_id', 'amount_paid', 'escrow_status', 'placement_status']);
  const id = 'APP_' + new Date().getTime();
  
  sheet.appendRow([
    id,
    data.seekerId || 'SEEKER_' + new Date().getTime(),
    data.jobId,
    data.portfolioUrl || '',
    data.paymentId || 'UTR_' + new Date().getTime(),
    data.amount || '$100',
    'Held',
    'Applied'
  ]);
  
  return { success: true, applicationId: id };
}

/**
 * Subscribe newsletter email
 */
function handleSubscribeNewsletter(ss, data) {
  const sheet = getOrCreateSheet(ss, 'Newsletter_Subscriptions', ['email', 'date_subscribed']);
  
  // Simple checks
  const values = sheet.getDataRange().getValues();
  for (let i = 0; i < values.length; i++) {
    if (values[i][0] === data.email) {
      return { success: true, message: 'Already subscribed' };
    }
  }
  
  sheet.appendRow([data.email, new Date().toISOString()]);
  return { success: true };
}

/**
 * Submit contact form
 */
function handleSubmitContact(ss, data) {
  const sheet = getOrCreateSheet(ss, 'Contact_Messages', ['name', 'email', 'subject', 'message', 'date_submitted']);
  sheet.appendRow([
    data.name,
    data.email,
    data.subject || 'General inquiry',
    data.message,
    new Date().toISOString()
  ]);
  return { success: true };
}

/**
 * Submit referral payout request / UTR
 */
function handleSubmitReferralUTR(ss, data) {
  const sheet = getOrCreateSheet(ss, 'Seeker_Requests', ['request_id', 'seeker_id', 'job_id', 'giver_id', 'transaction_id', 'payment_status', 'match_status']);
  const id = 'REQ_' + new Date().getTime();
  
  sheet.appendRow([
    id,
    'SEEKER_' + new Date().getTime(),
    data.jobId || 'JOB_ANY',
    data.giverId || 'GIVER_1',
    data.utr,
    'Verified',
    'Pending'
  ]);
  
  return { success: true, requestId: id };
}

/**
 * Admin Panel: Read any sheet data
 */
function handleAdminGetSheetData(ss, data) {
  if (data.adminSecret !== 'admin-master-key') {
    return { success: false, error: 'Unauthorized access' };
  }
  
  const sheetName = data.sheetName;
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) return { success: false, error: 'Sheet not found: ' + sheetName };
  
  const rangeValues = sheet.getDataRange().getValues();
  const headers = rangeValues[0] || [];
  const rows = [];
  
  for (let i = 1; i < rangeValues.length; i++) {
    const row = {};
    for (let j = 0; j < headers.length; j++) {
      row[headers[j]] = rangeValues[i][j];
    }
    rows.push(row);
  }
  
  return { success: true, headers: headers, rows: rows };
}

/**
 * Admin Panel: Edit/Delete/Insert a row
 */
function handleAdminUpdateData(ss, data) {
  if (data.adminSecret !== 'admin-master-key') {
    return { success: false, error: 'Unauthorized access' };
  }
  
  const sheetName = data.sheetName;
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) return { success: false, error: 'Sheet not found' };
  
  const actionType = data.type; // 'add', 'edit', 'delete'
  const headers = sheet.getDataRange().getValues()[0] || [];
  
  if (actionType === 'add') {
    const rowValues = headers.map(h => data.row[h] || '');
    sheet.appendRow(rowValues);
    return { success: true };
  }
  
  const keyColumn = data.keyColumn; // e.g. 'seeker_id' or 'job_id'
  const keyValue = data.keyValue;
  
  const keyColIndex = headers.indexOf(keyColumn);
  if (keyColIndex === -1) return { success: false, error: 'Key column not found' };
  
  const rangeValues = sheet.getDataRange().getValues();
  let rowIndex = -1;
  for (let i = 1; i < rangeValues.length; i++) {
    if (rangeValues[i][keyColIndex] == keyValue) {
      rowIndex = i + 1; // 1-indexed header + row values
      break;
    }
  }
  
  if (rowIndex === -1) return { success: false, error: 'Row not found matching key value' };
  
  if (actionType === 'delete') {
    sheet.deleteRow(rowIndex);
    return { success: true };
  } else if (actionType === 'edit') {
    for (let j = 0; j < headers.length; j++) {
      const headerName = headers[j];
      if (data.row[headerName] !== undefined) {
        sheet.getRange(rowIndex, j + 1).setValue(data.row[headerName]);
      }
    }
    return { success: true };
  }
  
  return { success: false, error: 'Invalid update operation' };
}
