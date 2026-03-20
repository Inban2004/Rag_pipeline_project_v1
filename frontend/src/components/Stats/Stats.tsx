import { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import styles from './Stats.module.css';

interface StatItem {
  value: number;
  suffix: string;
  label: string;
}

interface StatsProps {
  stats?: StatItem[];
}

const DEFAULT_STATS: StatItem[] = [
  { value: 500, suffix: '+', label: 'Visas Approved' },
  { value: 20, suffix: '+', label: 'Countries Covered' },
  { value: 1000, suffix: '+', label: 'Happy Travelers' },
];

function useCountUp(target: number, trigger: boolean, duration = 2000) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!trigger) return;
    let start = 0;
    const step = target / (duration / 16);
    const timer = setInterval(() => {
      start += step;
      if (start >= target) {
        setCount(target);
        clearInterval(timer);
      } else {
        setCount(Math.floor(start));
      }
    }, 16);
    return () => clearInterval(timer);
  }, [trigger, target, duration]);
  return count;
}

function StatCard({ stat, inView }: { stat: StatItem; inView: boolean }) {
  const count = useCountUp(stat.value, inView);
  return (
    <div className={styles.stat}>
      <div className={styles.statNumber}>
        {count}{stat.suffix}
      </div>
      <div className={styles.statLabel}>{stat.label}</div>
    </div>
  );
}

function Stats({ stats = DEFAULT_STATS }: StatsProps) {
  const ref = useRef<HTMLDivElement>(null);
  const [inView, setInView] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setInView(true); },
      { threshold: 0.3 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <section className={styles.section} id="about" ref={ref}>
      <div className={styles.container}>
        <motion.div
          className={styles.header}
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <span className="section-label" style={{ color: 'rgba(255,255,255,0.7)' }}>Why Choose Us</span>
          <h2 className="section-title">Trusted by Thousands</h2>
          <p className={`section-subtitle ${styles.headerSubtitle}`}>
            Our track record speaks for itself. We've helped thousands achieve their travel and career goals.
          </p>
        </motion.div>
        <div className={styles.grid}>
          {stats.map((stat) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
            >
              <StatCard stat={stat} inView={inView} />
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default Stats;
