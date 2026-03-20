import styles from './Footer.module.css';

interface FooterProps {
  brandName?: string;
}

function Footer({ brandName = 'AlfaOverseas' }: FooterProps) {
  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        <div className={styles.top}>
          <div>
            <div className={styles.brand}>
              {brandName.slice(0, 6)}<span className={styles.brandAccent}>{brandName.slice(6)}</span>
            </div>
            <p className={styles.brandDesc}>
              Your trusted partner for visa consultation and travel planning. Making global opportunities accessible to everyone.
            </p>
          </div>
          <div>
            <div className={styles.colTitle}>Services</div>
            <ul className={styles.links}>
              <li>Travel Planning</li>
              <li>Student Visa</li>
              <li>Work Visa</li>
              <li>Tourist Visa</li>
            </ul>
          </div>
          <div>
            <div className={styles.colTitle}>Contact</div>
            <ul className={styles.links}>
              <li>info@alfaoverseas.com</li>
              <li>+1 (555) 123-4567</li>
              <li>123 Travel Street, Suite 100</li>
              <li>New York, NY 10001</li>
            </ul>
          </div>
        </div>
        <div className={styles.divider} />
        <div className={styles.bottom}>
          <span className={styles.copyright}>© {new Date().getFullYear()} {brandName}. All rights reserved.</span>
          <span className={styles.license}>Licensed Travel & Visa Consultancy • Reg. No. ALFA-2024-001</span>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
