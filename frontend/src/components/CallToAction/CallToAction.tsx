import { motion } from 'framer-motion';
import styles from './CallToAction.module.css';

interface CallToActionProps {
  title?: string;
  subtitle?: string;
}

function CallToAction({
  title = 'Start Your Journey Today',
  subtitle = 'Get a free consultation with our visa experts. We will guide you through every step of the process.',
}: CallToActionProps) {
  const scrollTo = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section className={styles.section} id="contact">
      <motion.div
        className={styles.container}
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-100px' }}
        transition={{ duration: 0.6 }}
      >
        <span className="section-label">Ready?</span>
        <h2 className={`section-title ${styles.title}`}>{title}</h2>
        <p className={`section-subtitle ${styles.subtitle}`}>{subtitle}</p>
        <div className={styles.buttons}>
          <button className="btn btn-primary btn-lg" onClick={() => scrollTo('hero')}>
            Book Free Consultation
          </button>
          <button className="btn btn-outline btn-lg" onClick={() => scrollTo('services')}>
            View Our Services
          </button>
        </div>
      </motion.div>
    </section>
  );
}

export default CallToAction;
