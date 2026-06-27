import os
import subprocess

# Define paths
cwd = r"c:\Users\damak\Downloads\CodeNow\portfolio"
output_dir = os.path.join(cwd, "output", "pdf")
os.makedirs(output_dir, exist_ok=True)

brief_html_path = os.path.join(cwd, "output", "executive_brief.html")
ats_html_path = os.path.join(cwd, "output", "ats_resume.html")

brief_pdf_path = os.path.join(output_dir, "damak-varshney-executive-brief.pdf")
ats_pdf_path = os.path.join(output_dir, "damak-kumar-varshney-resume.pdf")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# ----------------- 1. Executive Brief HTML & CSS -----------------
# This visual brief matches the website: deep navy black header, electric blue accents, visual timeline.
brief_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Damak Varshney - Executive Brief</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&family=PT+Sans:wght@400;700&display=swap" rel="stylesheet">
  <style>
    @page {
      size: letter;
      margin: 0;
    }
    *, *::before, *::after {
      box-sizing: border-box;
    }
    body {
      font-family: 'DM Sans', sans-serif;
      color: #0F172A;
      background-color: #FFFFFF;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact;
      font-size: 9pt;
      line-height: 1.4;
    }
    a {
      color: #2563EB;
      text-decoration: none;
    }
    .page {
      width: 8.5in;
      height: 11in;
      position: relative;
      box-sizing: border-box;
      background-color: #FFFFFF;
      page-break-after: always;
      overflow: hidden;
    }
    .p-padded {
      padding: 0.4in 0.6in;
    }
    /* Header background: #080C10 */
    .header-content {
      background-color: #080C10;
      color: #FFFFFF;
      padding: 0.45in 0.6in;
    }
    .header-content h1 {
      font-family: 'PT Sans', sans-serif;
      font-size: 26pt;
      margin: 0 0 4px 0;
      font-weight: 700;
      letter-spacing: -0.5px;
      color: #FFFFFF;
    }
    .header-content .subtitle {
      color: #2563EB; /* Accent color: #2563EB */
      font-family: 'PT Sans', sans-serif;
      font-size: 12pt;
      font-weight: 700;
      margin-bottom: 12px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }
    .header-content .contacts {
      font-size: 8pt;
      color: #94A3B8;
      display: flex;
      gap: 15px;
    }
    .header-content .contacts span {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    /* Summary */
    .summary-text {
      font-size: 9pt;
      color: #334155;
      line-height: 1.5;
      margin-bottom: 0.25in;
      font-weight: 300;
    }

    /* Metrics Row */
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 10px;
      margin-bottom: 0.3in;
    }
    .metric-box {
      background-color: #F8FAFC;
      border: 1px solid #CBD5E1; /* Borders: #CBD5E1 */
      border-radius: 8px;
      padding: 8px;
      text-align: center;
    }
    .metric-value {
      font-size: 14pt;
      font-weight: 700;
      color: #2563EB; /* Accent color: #2563EB */
      font-family: 'PT Sans', sans-serif;
    }
    .metric-label {
      font-size: 7pt;
      font-weight: 700;
      color: #0F172A; /* Body text: #0F172A */
      margin-top: 2px;
      text-transform: uppercase;
      letter-spacing: 0.2px;
    }

    /* Sections */
    .section-title {
      font-family: 'PT Sans', sans-serif;
      font-size: 11pt;
      font-weight: 700;
      color: #2563EB; /* Section labels: #2563EB */
      border-bottom: 1.5px solid #CBD5E1; /* Borders: #CBD5E1 */
      padding-bottom: 3px;
      margin-top: 0;
      margin-bottom: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    /* Case Studies */
    .case-studies-container {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .case-card {
      border: 1px solid #E2E8F0;
      border-left: 3px solid #2563EB;
      border-radius: 6px;
      padding: 10px 12px;
      background-color: #FCFDFE;
    }
    .case-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }
    .case-title {
      font-family: 'PT Sans', sans-serif;
      font-size: 10.5pt;
      font-weight: 700;
      color: #0F172A;
    }
    .case-tag {
      font-size: 7.5pt;
      font-weight: 700;
      color: #10B981;
      background-color: #ECFDF5;
      padding: 2px 6px;
      border-radius: 4px;
    }
    .case-metrics {
      display: flex;
      gap: 15px;
      font-size: 8pt;
      color: #334155;
      margin-bottom: 4px;
      font-weight: 500;
    }
    .case-desc {
      font-size: 8pt;
      color: #475569;
      margin: 0;
      font-weight: 300;
    }

    /* Columns for page 2 */
    .two-column {
      display: grid;
      grid-template-columns: 3.5in 1.9in;
      gap: 25px;
    }

    /* Capabilities list */
    .capabilities-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .capability-item {
      font-size: 8pt;
      color: #334155;
    }
    .capability-name {
      font-weight: 700;
      color: #0F172A;
      margin-bottom: 1px;
    }

    /* Career Journey timeline */
    .timeline-container {
      position: relative;
      padding-left: 18px;
      margin-top: 8px;
    }
    .timeline-line {
      position: absolute;
      left: 4px;
      top: 4px;
      bottom: 4px;
      width: 1.5px;
      background-color: #CBD5E1;
    }
    .timeline-item {
      position: relative;
      margin-bottom: 14px;
    }
    .timeline-item:last-child {
      margin-bottom: 0;
    }
    .timeline-dot {
      position: absolute;
      left: -17.5px;
      top: 3px;
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background-color: #2563EB;
      border: 1.5px solid #FFFFFF;
      box-shadow: 0 0 0 1.5px #2563EB;
    }
    .timeline-role {
      font-family: 'PT Sans', sans-serif;
      font-size: 8.5pt;
      font-weight: 700;
      color: #0F172A;
      line-height: 1.2;
    }
    .timeline-meta {
      font-size: 7pt;
      color: #64748B;
      margin-top: 1px;
      font-weight: 500;
    }
    .timeline-company {
      color: #2563EB;
    }

    /* Awards List */
    .awards-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .award-item {
      font-size: 8pt;
      color: #334155;
      line-height: 1.3;
    }
    .award-title {
      font-weight: 700;
      color: #0F172A;
    }
    .award-org {
      color: #64748B;
      font-size: 7.5pt;
    }

    /* Footer styling */
    .footer-content {
      position: absolute;
      bottom: 0.3in;
      left: 0.6in;
      right: 0.6in;
      border-top: 1px solid #CBD5E1;
      padding-top: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 7.5pt;
      color: #64748B;
    }
  </style>
</head>
<body>

  <!-- PAGE 1: HEADER, METRICS, CASE STUDIES -->
  <div class="page">
    <div class="header-content">
      <h1>DAMAK KUMAR VARSHNEY</h1>
      <div class="subtitle">AI Product Manager | Business Transformation | Enterprise AI Strategy</div>
      <div class="contacts">
        <span>📍 Gurugram, India</span>
        <span>✉️ damakvarshney@gmail.com</span>
        <span>🔗 linkedin.com/in/damak-varshney</span>
        <span>🌐 damak-varshney.vercel.app</span>
      </div>
    </div>

    <div class="p-padded" style="padding-top: 0;">
      <div class="summary-text">
        Quantified outcomes leader with 5+ years of experience transforming financial services operations. Shipped 5 AI-powered products at OSTTRA (KKR portfolio) delivering 16+ FTE savings, 55% faster onboarding, and 80%+ organic adoption across 1,500+ active global users. Combines technical build depth (Vertex AI RAG pipelines, Google Apps Script serverless engines) with financial-domain expertise (OTC markets, credit analysis, and regulatory compliance).
      </div>

      <div class="section-title">Transformation Impact Snapshot</div>
      <div class="metrics-grid">
        <div class="metric-box">
          <div class="metric-value">16+</div>
          <div class="metric-label">FTE Saved</div>
        </div>
        <div class="metric-box">
          <div class="metric-value">5</div>
          <div class="metric-label">AI Products</div>
        </div>
        <div class="metric-box">
          <div class="metric-value">1,500+</div>
          <div class="metric-label">Active Users</div>
        </div>
        <div class="metric-box">
          <div class="metric-value">55%</div>
          <div class="metric-label">Faster Onboarding</div>
        </div>
        <div class="metric-box">
          <div class="metric-value">70%+</div>
          <div class="metric-label">AI Resolution</div>
        </div>
      </div>

      <div class="section-title">Selected Case Studies</div>
      <div class="case-studies-container">
        
        <div class="case-card">
          <div class="case-header">
            <span class="case-title">NEXUS — Global Capacity Intelligence Platform</span>
            <span class="case-tag">Live · 1,500+ Users</span>
          </div>
          <div class="case-metrics">
            <span>📊 Impact: 80%+ Adoption</span>
            <span>⚡ Cycle Time: Reduced by 45%</span>
          </div>
          <p class="case-desc">
            Consolidated 150+ fragmented regional operational tracking spreadsheets into a single, real-time resourcing system with role-based access control. Implemented predictive workforce modeling and Looker analytics, allowing leadership to dynamically optimize cross-training, resource utilization, and client allocations.
          </p>
        </div>

        <div class="case-card">
          <div class="case-header">
            <span class="case-title">Dot & ODA — RAG-Based Salesforce AI Assistants</span>
            <span class="case-tag">Live · 70% Self-Service</span>
          </div>
          <div class="case-metrics">
            <span>🤖 Tech: Vertex AI + Gemini</span>
            <span>🛡️ Saved: 4+ FTE Annually</span>
          </div>
          <p class="case-desc">
            Designed and deployed intelligent support assistants within Salesforce cases. Trained RAG agents on proprietary reference data, OTC market operations, and LSEG Pricing workflows, reducing routine information-request inquiries from 16% to 3% and accelerating triage cycle time by 70%.
          </p>
        </div>

        <div class="case-card">
          <div class="case-header">
            <span class="case-title">SOX Compliance & Access Validation Engine</span>
            <span class="case-tag">Live · 100% Audit-Ready</span>
          </div>
          <div class="case-metrics">
            <span>⚙️ Tech: Serverless Apps Script</span>
            <span>⏱️ Speed: 45 to 5 days (90% reduction)</span>
          </div>
          <p class="case-desc">
            Replaced manual user entitlement checks with a serverless, zero-cost access validation engine. Automated workflow emails and audit evidence gathering, saving 4.1 FTEs per review cycle with zero audit findings.
          </p>
        </div>

      </div>
    </div>

    <div class="footer-content">
      <span>Damak Kumar Varshney — Executive Brief</span>
      <span>Page 1 of 2</span>
    </div>
  </div>

  <!-- PAGE 2: CAPABILITIES, RECOGNITION, CAREER TIMELINE -->
  <div class="page p-padded">
    <div style="height: 9.6in;"> <!-- Constraint height for column flow -->
      <div class="two-column">
        
        <!-- Left: Capabilities & Timeline -->
        <div>
          <div class="section-title">Capabilities & transformation stack</div>
          <div class="capabilities-list">
            
            <div class="capability-item">
              <div class="capability-name">AI & LLM Stack</div>
              Vertex AI, Google Gemini, Enterprise RAG Architecture, Vector Embeddings, Prompt Engineering, Agentic Workflows, LLM-powered Automation, AI Product Strategy
            </div>

            <div class="capability-item">
              <div class="capability-name">Cloud & Data Stack</div>
              Python, SQL, Google BigQuery, ChromaDB, Google Cloud Platform (GCP), Serverless Architectures, Google Apps Script, REST API Integrations
            </div>

            <div class="capability-item">
              <div class="capability-name">Product & Operations</div>
              Salesforce Administration, Jira/Confluence, Looker Studio, Power BI, Change Management, Operating Model Design, User Adoption Strategy
            </div>

            <div class="capability-item">
              <div class="capability-name">Methodologies & Domains</div>
              Lean Six Sigma, Agile/Scrum, LUMA Design Thinking, Process Reengineering, OTC Markets, KYC/AML Compliance, SOX Entitlement Audits
            </div>

          </div>

          <div class="section-title" style="margin-top: 25px;">CAREER JOURNEY</div>
          <div class="timeline-container">
            <div class="timeline-line"></div>
            
            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-role">Associate, AI Strategy & Ops</div>
              <div class="timeline-meta">Apr 2025 – Present | <span class="timeline-company">OSTTRA (KKR Portfolio)</span> | Gurugram</div>
            </div>

            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-role">Senior OpEx Analyst</div>
              <div class="timeline-meta">Feb 2024 – Dec 2024 | <span class="timeline-company">OSTTRA</span> | Gurugram</div>
            </div>

            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-role">Academic & Finance Immersion</div>
              <div class="timeline-meta">2022 – 2024 | <span class="timeline-company">ICFAI Business School + IFHE Hyderabad</span></div>
            </div>

            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-role">React Native Developer</div>
              <div class="timeline-meta">2020 – 2022 | <span class="timeline-company">RPQ IT Services</span> | Delhi NCR</div>
            </div>

          </div>

          <div class="section-title" style="margin-top: 25px;">Education</div>
          <div class="capabilities-list">
            <div class="capability-item" style="margin-bottom: 2px;">
              <span style="font-weight: 700; color: #0F172A;">PGPM (Finance & Analytics)</span> — ICFAI Business School, Gurgaon (2022-2024) | CGPA: 9.0/10
            </div>
            <div class="capability-item" style="margin-bottom: 2px;">
              <span style="font-weight: 700; color: #0F172A;">MBA (Finance & Analytics)</span> — IFHE Hyderabad (Online, 2022-2024) | CGPA: 8.75/10
            </div>
            <div class="capability-item">
              <span style="font-weight: 700; color: #0F172A;">BCA (Computer Science)</span> — Birla Institute of Technology, Mesra (2017-2020)
            </div>
          </div>

        </div>

        <!-- Right: Recognition & Certs -->
        <div>
          <div class="section-title">RECOGNITION</div>
          <div class="awards-list">
            
            <div class="award-item">
              <div class="award-title">Times of India Feature</div>
              <div class="award-org">InspireTech 2025</div>
              Recognized for enterprise AI chatbot and Salesforce auto-triaging models.
            </div>

            <div class="award-item">
              <div class="award-title">Highflyer Award</div>
              <div class="award-org">OSTTRA Q1 2026</div>
              Awarded for Looker analytics and Salesforce routing tools saving manual effort.
            </div>

            <div class="award-item">
              <div class="award-title">Trendsetter Award</div>
              <div class="award-org">OSTTRA Q1 2025</div>
              Awarded for SOX Compliance automation engine saving 4.1 FTE.
            </div>

            <div class="award-item">
              <div class="award-title">1st Prize, Design Thinking</div>
              <div class="award-org">Protiviti Challenge 2023</div>
              Won first place for user-centered process design optimization.
            </div>

            <div class="award-item">
              <div class="award-title">Spot Awards</div>
              <div class="award-org">OSTTRA 2024 - 2026</div>
              Received multiple awards for rapid tooling shipping.
            </div>

          </div>

          <div class="section-title" style="margin-top: 25px;">Certifications</div>
          <div class="awards-list" style="gap: 5px;">
            <div class="award-item">
              <div style="font-weight: 700; color: #0F172A;">Google Data Analytics</div>
              <div class="award-org">Google (2022)</div>
            </div>
            <div class="award-item">
              <div style="font-weight: 700; color: #0F172A;">Certified Data Scientist</div>
              <div class="award-org">Henry Harvin (2022)</div>
            </div>
            <div class="award-item">
              <div style="font-weight: 700; color: #0F172A;">SQL Certification</div>
              <div class="award-org">DataCamp (2022)</div>
            </div>
          </div>

        </div>

      </div>
    </div>

    <div class="footer-content">
      <span>Damak Kumar Varshney — Executive Brief</span>
      <span>Page 2 of 2</span>
    </div>
  </div>

</body>
</html>
"""

# ----------------- 2. ATS-Optimized Resume HTML & CSS -----------------
# Fully revised: tighter margins, phone number, no arrows, varied verbs, semicolons, compact bullets, pipe-separated skills, correct section order.
ats_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Damak Kumar Varshney - Resume</title>
  <style>
    @page {
      size: letter;
      margin: 0.6in 0.65in;
    }
    body {
      font-family: 'Calibri', 'Arial', sans-serif;
      color: #000000;
      background-color: #FFFFFF;
      margin: 0;
      padding: 0;
      font-size: 10pt;
      line-height: 1.2;
    }
    .header-section {
      text-align: center;
      margin-bottom: 8px;
    }
    .name {
      font-size: 15pt;
      font-weight: bold;
      text-transform: uppercase;
      margin-bottom: 2px;
      letter-spacing: 0.5px;
    }
    .contact-info {
      font-size: 9pt;
      margin-bottom: 2px;
    }
    .headline {
      font-size: 10pt;
      font-weight: bold;
      text-transform: uppercase;
      border-bottom: 1px solid #000000;
      padding-bottom: 2px;
      margin-top: 4px;
      margin-bottom: 8px;
    }
    .section-title {
      font-size: 10.5pt;
      font-weight: bold;
      text-transform: uppercase;
      border-bottom: 1px solid #000000;
      margin-top: 9px;
      margin-bottom: 4px;
      padding-bottom: 1px;
    }
    .summary-text {
      font-size: 9.5pt;
      margin-bottom: 0;
      text-align: justify;
      line-height: 1.25;
    }
    .job-entry {
      margin-bottom: 7px;
    }
    .job-header {
      font-weight: bold;
      font-size: 10pt;
      display: flex;
      justify-content: space-between;
    }
    .job-meta {
      font-style: italic;
      font-size: 9pt;
      display: flex;
      justify-content: space-between;
      margin-bottom: 2px;
    }
    ul {
      margin: 2px 0 0 0;
      padding-left: 14px;
    }
    li {
      margin-bottom: 2px;
      text-align: justify;
      font-size: 9.5pt;
      line-height: 1.2;
    }
    .education-line {
      font-size: 9.5pt;
      margin-bottom: 2px;
      line-height: 1.2;
    }
    .skills-category {
      margin-bottom: 2px;
      font-size: 9.5pt;
      line-height: 1.2;
    }
    .skills-label {
      font-weight: bold;
    }
    .cert-line {
      font-size: 9.5pt;
      margin-bottom: 2px;
      line-height: 1.2;
    }
    .recog-list {
      margin: 2px 0 0 0;
      padding-left: 14px;
    }
    .recog-list li {
      font-size: 9.5pt;
      margin-bottom: 2px;
      line-height: 1.2;
    }
  </style>
</head>
<body>

  <div class="header-section">
    <div class="name">DAMAK KUMAR VARSHNEY</div>
    <div class="contact-info">
      Gurugram, India &nbsp;|&nbsp; +91-8077293920 &nbsp;|&nbsp; damakvarshney@gmail.com
    </div>
    <div class="contact-info">
      linkedin.com/in/damak-varshney &nbsp;|&nbsp; damak-varshney.vercel.app
    </div>
    <div class="headline">
      AI Product Manager | Business Transformation | Enterprise AI Strategy
    </div>
  </div>

  <div class="section-title">SUMMARY</div>
  <div class="summary-text">
    Shipped 5 AI products at OSTTRA (KKR Portfolio) generating 16+ FTE in savings and 80%+ adoption across 1,500+ users. Combines technical depth, financial-services expertise, and enterprise adoption discipline. Outcomes include 55% faster onboarding, 13% case-volume cut, and fully automated SOX compliance.
  </div>

  <div class="section-title">WORK EXPERIENCE</div>

  <div class="job-entry">
    <div class="job-header">
      <span>Associate, AI Strategy &amp; Ops Excellence</span>
      <span>Apr 2025 &ndash; Present</span>
    </div>
    <div class="job-meta">
      <span>OSTTRA (KKR Portfolio Company) | Gurugram, India</span>
    </div>
    <ul>
      <li>Architected NEXUS global capacity platform consolidating 150+ spreadsheets using Python predictive modeling and Looker; drove 80%+ adoption across 1,500+ users and compressed planning cycles 45%.</li>
      <li>Designed Dot and ODA, RAG-based Salesforce assistants powered by Vertex AI; decreased routine client information cases from 16% to 3% and freed 4+ FTE annually for strategic work.</li>
      <li>Led intelligent KYC and onboarding automation with AI checklist extraction and reference registry APIs; shortened cycle time 55% from 18 to 8 days with 100% audit traceability.</li>
      <li>Rolled out 25+ Salesforce auto-triaging enhancements including AI categorization and entity screening; recovered 4+ FTE annually and accelerated case resolution by 40%.</li>
    </ul>
  </div>

  <div class="job-entry">
    <div class="job-header">
      <span>Senior Operational Excellence Analyst</span>
      <span>Feb 2024 &ndash; Dec 2024</span>
    </div>
    <div class="job-meta">
      <span>OSTTRA | Gurugram, India</span>
    </div>
    <ul>
      <li>Engineered SOX Compliance automation using Google Apps Script; eliminated 4.1 FTEs of manual audit work, achieved 100% compliance, and compressed audit cycle from 45 to 5 days.</li>
      <li>Delivered 10+ continuous improvement initiatives applying Lean Six Sigma and Agile across client services and trading operations; unlocked 2+ FTE in quantitative savings.</li>
      <li>Directed Microsoft to Google Workspace migration during Tel Aviv-to-India transition; removed VDI dependency, cut access latency 40%, and freed 0.4 FTEs.</li>
    </ul>
  </div>

  <div class="job-entry">
    <div class="job-header">
      <span>Credit Analyst Intern</span>
      <span>Feb 2023 &ndash; Apr 2023</span>
    </div>
    <div class="job-meta">
      <span>Kotak Mahindra Bank | Delhi NCR, India</span>
    </div>
    <ul>
      <li>Evaluated 20+ MSME credit applications analyzing financial statements and working capital dynamics; delivered recommendations with 95%+ accuracy contributing to $3M+ underwriting decisions.</li>
    </ul>
  </div>

  <div class="job-entry">
    <div class="job-header">
      <span>React Native Developer</span>
      <span>Apr 2021 &ndash; May 2022</span>
    </div>
    <div class="job-meta">
      <span>RPQ IT Services | Remote, India</span>
    </div>
    <ul>
      <li>Developed 5+ production mobile applications using React Native; designed UI/UX wireframes in Figma and shipped cross-platform iOS and Android builds.</li>
    </ul>
  </div>

  <div class="section-title">EDUCATION</div>
  <div class="education-line"><strong>Post Graduate Programme, Finance &amp; Analytics</strong> &mdash; ICFAI Business School, Gurgaon | 2022 &ndash; Apr 2024 | CGPA: 9.0/10</div>
  <div class="education-line"><strong>MBA, Finance &amp; Analytics</strong> (Online, concurrent with OSTTRA role) &mdash; IFHE Hyderabad | 2022 &ndash; Jul 2024 | CGPA: 8.75/10</div>
  <div class="education-line"><strong>Bachelor of Computer Applications</strong> &mdash; Birla Institute of Technology, Mesra | 2017 &ndash; 2020 | CGPA: 7.52/10</div>

  <div class="section-title">SKILLS</div>
  <div class="skills-category"><span class="skills-label">AI and LLM Stack:</span> Vertex AI | Google Gemini | RAG Pipelines | Vector Embeddings | Prompt Engineering | Agentic Workflows | LLM-Powered Automation</div>
  <div class="skills-category"><span class="skills-label">Cloud and Data:</span> Python | SQL | Google BigQuery | ChromaDB | Google Cloud Platform | Looker Studio | Power BI</div>
  <div class="skills-category"><span class="skills-label">Product and Tools:</span> Salesforce | Jira | Confluence | Google AppSheet | Google Apps Script | REST APIs</div>
  <div class="skills-category"><span class="skills-label">Methodologies:</span> Lean Six Sigma | Agile/Scrum | LUMA Design Thinking | Process Reengineering | Change Management</div>
  <div class="skills-category"><span class="skills-label">Financial Domain:</span> OTC Markets | Reference Data | KYC/AML | SOX Compliance | Financial Services Infrastructure</div>

  <div class="section-title">CERTIFICATIONS</div>
  <div class="cert-line">Google Data Analytics Professional Certificate, Google (2022)</div>
  <div class="cert-line">Certified Data Scientist, Henry Harvin Education (2022)</div>
  <div class="cert-line">SQL Certification, DataCamp (2022)</div>

  <div class="section-title">RECOGNITION</div>
  <ul class="recog-list">
    <li>Featured in Times of India, InspireTech 2025 &mdash; Enterprise AI and Automation Systems</li>
    <li>Highflyer Award, OSTTRA Q1 2026 &mdash; Looker analytics and Salesforce auto-triaging impact</li>
    <li>Trendsetter Award, OSTTRA Q1 2025 &mdash; SOX Compliance automation</li>
    <li>1st Prize, LUMA Design Thinking Challenge, Protiviti 2023</li>
    <li>Multiple Quarterly Spot Awards, OSTTRA 2024 &ndash; 2026</li>
  </ul>

</body>
</html>
"""

# Write HTML files
with open(brief_html_path, "w", encoding="utf-8") as f:
    f.write(brief_html_content)
print(f"Written {brief_html_path}")

with open(ats_html_path, "w", encoding="utf-8") as f:
    f.write(ats_html_content)
print(f"Written {ats_html_path}")

# Compile HTML to PDF using headless Chrome
# Page layout configurations:
# --no-margins is NOT used, standard page formats are defined by CSS
print("Compiling Executive Brief to PDF...")
brief_cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={brief_pdf_path}",
    brief_html_path
]
subprocess.run(brief_cmd, check=True)
print(f"Successfully generated {brief_pdf_path}")

print("Compiling ATS Resume to PDF...")
ats_cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={ats_pdf_path}",
    ats_html_path
]
subprocess.run(ats_cmd, check=True)
print(f"Successfully generated {ats_pdf_path}")
