import { useState, useEffect } from 'react';
import styles from './Navbar.module.css';

interface NavbarProps {
  brandName?: string;
}

const NAV_LINKS = ['Services', 'Process', 'About', 'Testimonials', 'Contact'];

function Navbar({ brandName = 'AlfaOverseas' }: NavbarProps) {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const scrollTo = (id: string) => {
    document.getElementById(id.toLowerCase())?.scrollIntoView({ behavior: 'smooth' });
    setMobileOpen(false);
  };

  return (
    <>
      <nav className={`${styles.navbar} ${scrolled ? styles.scrolled : ''}`}>
        <div className={styles.container}>
          <span className={styles.logo}>
            {brandName.slice(0, 6)}<span className={styles.logoAccent}>{brandName.slice(6)}</span>
          </span>
          <div className={styles.nav}>
            {NAV_LINKS.map((link) => (
              <button key={link} className={styles.navLink} onClick={() => scrollTo(link)}>
                {link}
              </button>
            ))}
            <button className={`btn btn-primary ${styles.ctaBtn}`} onClick={() => scrollTo('Contact')}>
              Get Started
            </button>
          </div>
          <button className={styles.mobileToggle} onClick={() => setMobileOpen(!mobileOpen)} aria-label="Toggle menu">
            <span className={styles.hamburger} />
          </button>
        </div>
      </nav>
      <div className={`${styles.mobileNav} ${mobileOpen ? styles.open : ''}`}>
        {NAV_LINKS.map((link) => (
          <button key={link} className={styles.mobileNavLink} onClick={() => scrollTo(link)}>
            {link}
          </button>
        ))}
        <button className="btn btn-primary" onClick={() => scrollTo('Contact')}>
          Get Started
        </button>
      </div>
    </>
  );
}

export default Navbar;
