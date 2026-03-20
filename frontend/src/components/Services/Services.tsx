import { motion } from 'framer-motion';
import styles from './Services.module.css';

interface ServiceItem {
  icon: string;
  title: string;
  description: string;
}

interface ServicesProps {
  services?: ServiceItem[];
}

const DEFAULT_SERVICES: ServiceItem[] = [
  {
    icon: '✈️',
    title: 'Travel Planning',
    description: 'Comprehensive travel itineraries, flight bookings, hotel reservations, and travel insurance — all tailored to your needs.',
  },
  {
    icon: '🎓',
    title: 'Student Visa',
    description: 'Expert guidance for student visa applications to top universities worldwide. We handle documentation, interviews, and follow-ups.',
  },
  {
    icon: '💼',
    title: 'Work Visa',
    description: 'Streamlined work visa processing for professionals. From eligibility assessment to final approval, we have got you covered.',
  },
  {
    icon: '🧩',
    title: 'New Service Placeholder',
    description: 'Reserved space for an upcoming service card. Replace this content whenever you are ready to expand the offering.',
  },
  {
    icon: '✨',
    title: 'Future Service Placeholder',
    description: 'Another placeholder card so you can grow the services carousel without changing the section layout later on.',
  },
];

function Services({ services = DEFAULT_SERVICES }: ServicesProps) {
  return (
    <section className={styles.section} id="services">
      <div className={styles.container}>
        <motion.div
          className={styles.header}
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ duration: 0.6 }}
        >
          <span className="section-label">What We Offer</span>
          <h2 className="section-title">Our Services</h2>
          <p className={`section-subtitle ${styles.subtitle}`}>
            From visa applications to complete travel planning, we provide end-to-end solutions for your journey.
          </p>
        </motion.div>
        <div className={styles.scrollViewport}>
          <div className={styles.grid}>
            {services.map((service, i) => (
              <motion.div
                key={service.title}
                className={styles.card}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-80px' }}
                transition={{ duration: 0.5, delay: i * 0.15 }}
              >
                <div className={styles.iconWrap}>{service.icon}</div>
                <h3 className={styles.cardTitle}>{service.title}</h3>
                <p className={styles.cardDesc}>{service.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

export default Services;
