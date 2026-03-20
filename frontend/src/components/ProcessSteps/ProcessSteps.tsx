import { motion } from 'framer-motion';
import styles from './ProcessSteps.module.css';

interface Step {
  icon: string;
  title: string;
  description: string;
}

interface ProcessStepsProps {
  steps?: Step[];
}

const DEFAULT_STEPS: Step[] = [
  { icon: '💬', title: 'Consultation', description: 'Free initial consultation to understand your goals and requirements.' },
  { icon: '📋', title: 'Document Prep', description: 'We help you gather and prepare all necessary documentation.' },
  { icon: '📤', title: 'Submission', description: 'We submit your application and track it every step of the way.' },
  { icon: '✅', title: 'Approval', description: 'We follow up and ensure your application gets approved smoothly.' },
  { icon: '🌍', title: 'Travel', description: 'You are all set! Time to embark on your journey with confidence.' },
];

function ProcessSteps({ steps = DEFAULT_STEPS }: ProcessStepsProps) {
  return (
    <section className={styles.section} id="process">
      <div className={styles.container}>
        <motion.div
          className={styles.header}
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ duration: 0.6 }}
        >
          <span className="section-label">How It Works</span>
          <h2 className="section-title">Our Simple Process</h2>
          <p className={`section-subtitle ${styles.subtitle}`}>
            We've streamlined the visa and travel process into five easy steps.
          </p>
        </motion.div>
        <div className={styles.steps}>
          {steps.map((step, i) => (
            <motion.div
              key={step.title}
              className={styles.step}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-60px' }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
            >
              <div className={styles.stepNumber}>{i + 1}</div>
              <div className={styles.connector} />
              <div className={styles.stepIcon}>{step.icon}</div>
              <h3 className={styles.stepTitle}>{step.title}</h3>
              <p className={styles.stepDesc}>{step.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default ProcessSteps;
