
(function() {
  const canvas = document.getElementById('pixel-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width = canvas.width = window.innerWidth;
  let height = canvas.height = window.innerHeight;

  let particles = [];
  const spacing = 40; // pixel spacing between points
  const mouse = { x: null, y: null, radius: 100 }; // mouse radius of influence

  class Particle {
    constructor(x, y) {
      this.x = x;
      this.y = y;
      this.baseX = x;
      this.baseY = y;
      this.vx = 0;
      this.vy = 0;
      this.size = 2; // small square pixel size
      this.density = (Math.random() * 20) + 15; // random density for varying spring speeds
    }

    draw() {
      // adapt color based on theme
      const isDark = document.documentElement.classList.contains('dark');
      ctx.fillStyle = isDark ? 'rgba(180, 83, 9, 0.45)' : 'rgba(180, 83, 9, 0.3)';
      ctx.fillRect(this.x, this.y, this.size, this.size);
    }

    update() {
      // spring force returning to original grid position
      let dx = this.baseX - this.x;
      let dy = this.baseY - this.y;
      
      // Hooke's law: F = -k * x
      let forceX = dx * 0.08;
      let forceY = dy * 0.08;

      // mouse interaction
      if (mouse.x !== null && mouse.y !== null) {
        let mdx = mouse.x - this.x;
        let mdy = mouse.y - this.y;
        let dist = Math.sqrt(mdx * mdx + mdy * mdy);
        
        if (dist < mouse.radius) {
          let pushForce = (mouse.radius - dist) / mouse.radius; // 0 to 1
          let angle = Math.atan2(mdy, mdx);
          forceX -= Math.cos(angle) * pushForce * this.density;
          forceY -= Math.sin(angle) * pushForce * this.density;
        }
      }

      // velocity with damping
      this.vx = (this.vx + forceX) * 0.82;
      this.vy = (this.vy + forceY) * 0.82;

      this.x += this.vx;
      this.y += this.vy;
    }
  }

  function init() {
    particles = [];
    const cols = Math.floor(width / spacing);
    const rows = Math.floor(height / spacing);
    
    const offsetX = (width - (cols * spacing)) / 2;
    const offsetY = (height - (rows * spacing)) / 2;

    for (let i = 0; i <= cols; i++) {
      for (let j = 0; j <= rows; j++) {
        let x = offsetX + (i * spacing);
        let y = offsetY + (j * spacing);
        particles.push(new Particle(x, y));
      }
    }
  }

  // track mouse events globally
  window.addEventListener('mousemove', function(e) {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
  });

  window.addEventListener('mouseleave', function() {
    mouse.x = null;
    mouse.y = null;
  });

  window.addEventListener('resize', function() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    init();
  });

  function animate() {
    ctx.clearRect(0, 0, width, height);
    for (let i = 0; i < particles.length; i++) {
      particles[i].update();
      particles[i].draw();
    }
    requestAnimationFrame(animate);
  }

  init();
  animate();
})();
