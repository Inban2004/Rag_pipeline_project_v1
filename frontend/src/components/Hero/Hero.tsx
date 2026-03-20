import { motion } from 'framer-motion';
import styles from './Hero.module.css';

interface HeroProps {
  bgImage: string;
}

function Hero({ bgImage }: HeroProps) {
  const scrollTo = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section className={styles.hero} id="hero">
      <img src={bgImage} alt="Travel destination" className={styles.bgImage} />
      <div className={styles.overlay} />
      <div className={styles.content}>
        <motion.span
          className={styles.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          Trusted by 1000+ Travelers
        </motion.span>
        <motion.h1
          className={styles.title}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.15 }}
        >
          Your Gateway to Global Opportunities
        </motion.h1>
        <motion.p
          className={styles.subtitle}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.3 }}
        >
          Expert visa consultation, seamless travel planning, and end-to-end support to make your dreams a reality.
        </motion.p>
        <motion.div
          className={styles.buttons}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.45 }}
        >
          <button className="btn btn-white btn-lg" onClick={() => scrollTo('services')}>
            Explore Services
          </button>
          <button className="btn btn-outline btn-lg" style={{ borderColor: '#fff', color: '#fff' }} onClick={() => scrollTo('contact')}>
            Free Consultation
          </button>
        </motion.div>
      </div>
    </section>
  );
}

export default Hero;
