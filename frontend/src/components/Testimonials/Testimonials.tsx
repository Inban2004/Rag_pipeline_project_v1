import { motion } from 'framer-motion';
import styles from './Testimonials.module.css';

interface Testimonial {
  name: string;
  role: string;
  avatar: string;
  quote: string;
}

interface TestimonialsProps {
  testimonials: Testimonial[];
}

function Testimonials({ testimonials }: TestimonialsProps) {
  return (
    <section className={styles.section} id="testimonials">
      <div className={styles.container}>
        <motion.div
          className={styles.header}
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ duration: 0.6 }}
        >
          <span className="section-label">Testimonials</span>
          <h2 className="section-title">What Our Clients Say</h2>
          <p className={`section-subtitle ${styles.subtitle}`}>
            Real stories from real travelers who trusted us with their journey.
          </p>
        </motion.div>
        <div className={styles.track}>
          {testimonials.map((t, i) => (
            <motion.div
              key={t.name}
              className={styles.card}
              initial={{ opacity: 0, x: 40 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, margin: '-60px' }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
            >
              <div className={styles.stars}>★★★★★</div>
              <p className={styles.quote}>"{t.quote}"</p>
              <div className={styles.author}>
                <img src={t.avatar} alt={t.name} className={styles.avatar} />
                <div>
                  <div className={styles.authorName}>{t.name}</div>
                  <div className={styles.authorRole}>{t.role}</div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default Testimonials;
