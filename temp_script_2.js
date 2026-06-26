
function app() {
  const SCRIPT_URL = 'YOUR_GOOGLE_WEB_APP_URL_HERE';

  return {
    dark: false,
    mm: false,
    sc: false,
    s: 'hero',
    showGreeting: false,
    greetingMsg: '',
    newsEmail: '',
    newsStatus: '',
    
    vibeIndex: 0,
    vibes: [
      { icon: '🎧', label: 'Listening', text: 'Lo-Fi Beats & Deep Focus' },
      { icon: '📚', label: 'Learning', text: 'RAG Architectures & Rust' },
      { icon: '☕', label: 'Status', text: 'Debugging the next big thing' }
    ],

    contactName: '',
    contactEmail: '',
    contactSubject: '',
    contactMessage: '',
    contactStatus: '',

    hackerMode: false,
    terminalLines: [
      { text: '> ./damak --init', color: 'text-emerald-500' },
      { text: 'Loading AI Strategy modules...', color: 'text-zinc-550' },
      { text: '[OK] Operational Excellence Engine', color: 'text-blue-500' },
      { text: '[OK] RAG Framework: "Dot" Active', color: 'text-blue-500' },
      { text: '> damak --status', color: 'text-emerald-500' },
      { text: 'Result: "Absolute Learner" mode engaged.', color: 'text-accent' }
    ],

    init() {
      // visit count & greeting
      let count = parseInt(localStorage.getItem('visit_count') || '0') + 1;
      localStorage.setItem('visit_count', count.toString());
      
      const counts = ["uno", "dos", "tres", "cuatro"];
      const adjectives = ["Explorer", "Builder", "Architect", "Thinker"];
      let countWord = count > 4 ? count.toString() : counts[count - 1];
      let adj = count > 4 ? "Professional" : adjectives[count - 1];
      
      this.greetingMsg = `¡Hola! Visita ${countWord}. Welcome back, ${adj}.`;
      this.showGreeting = true;
      setTimeout(() => this.showGreeting = false, 5000);

      // dark mode
      this.dark = localStorage.getItem('theme') === 'dark' ||
        (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
      this.$watch('dark', v => localStorage.setItem('theme', v ? 'dark' : 'light'));

      // scroll
      window.addEventListener('scroll', () => {
        this.sc = window.scrollY > 20;
        this.updateSection();
      }, { passive: true });

      // reveal
      const io = new IntersectionObserver(entries => {
        entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
      }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
      document.querySelectorAll('.reveal').forEach(el => io.observe(el));

      // year
      document.getElementById('yr').textContent = new Date().getFullYear();
    },

    updateSection() {
      const atBottom = (window.innerHeight + window.scrollY) >= document.body.scrollHeight - 60;
      if (atBottom) { this.s = 'contact'; return; }
      const ids = ['contact', 'blog', 'reviews', 'about', 'work', 'services', 'hero'];
      for (const id of ids) {
        const el = document.getElementById(id);
        if (el && window.scrollY >= el.offsetTop - 130) { this.s = id; return; }
      }
    },

    async subscribe() {
      if(!this.newsEmail) return;
      if (SCRIPT_URL.includes('YOUR_GOOGLE_WEB_APP_URL_HERE')) {
        this.newsStatus = 'error';
        return;
      }
      this.newsStatus = 'loading';
      try {
        await fetch(SCRIPT_URL, {
          method: 'POST',
          mode: 'no-cors',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ type: 'newsletter', email: this.newsEmail })
        });
        this.newsStatus = 'success';
        this.newsEmail = '';
      } catch (e) {
        this.newsStatus = 'error';
      }
    },

    async submitContact() {
      if(!this.contactEmail || !this.contactMessage) return;
      if (SCRIPT_URL.includes('YOUR_GOOGLE_WEB_APP_URL_HERE')) {
        this.contactStatus = 'error';
        return;
      }
      this.contactStatus = 'loading';
      try {
        await fetch(SCRIPT_URL, {
          method: 'POST',
          mode: 'no-cors',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            type: 'contact',
            name: this.contactName,
            email: this.contactEmail,
            subject: this.contactSubject,
            message: this.contactMessage
          })
        });
        this.contactStatus = 'success';
        this.contactName = ''; this.contactEmail = ''; this.contactSubject = ''; this.contactMessage = '';
      } catch (e) {
        this.contactStatus = 'error';
      }
    }
  }
}
