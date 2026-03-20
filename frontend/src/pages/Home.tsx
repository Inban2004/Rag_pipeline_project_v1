import Navbar from '../components/Navbar/Navbar';
import Hero from '../components/Hero/Hero';
import Services from '../components/Services/Services';
import ProcessSteps from '../components/ProcessSteps/ProcessSteps';
import Stats from '../components/Stats/Stats';
import Testimonials from '../components/Testimonials/Testimonials';
import CallToAction from '../components/CallToAction/CallToAction';
import Footer from '../components/Footer/Footer';
import { HERO_BG, TESTIMONIAL_1, TESTIMONIAL_2, TESTIMONIAL_3, TESTIMONIAL_4 } from '../assets/images/image';

const TESTIMONIALS = [
  {
    name: 'Sarah Mitchell',
    role: 'Student Visa Client',
    avatar: TESTIMONIAL_1,
    quote: 'AlfaOverseas made my student visa process incredibly smooth. I got accepted to my dream university in London and they handled everything!',
  },
  {
    name: 'James Rodriguez',
    role: 'Work Visa Client',
    avatar: TESTIMONIAL_2,
    quote: 'Professional, responsive, and knowledgeable. They helped me secure my work visa in record time. Highly recommended!',
  },
  {
    name: 'Kevin Tran',
    role: 'Travel Planning Client',
    avatar: TESTIMONIAL_3,
    quote: 'The travel planning service was exceptional. Every detail was taken care of, from flights to hotel bookings. A seamless experience.',
  },
  {
    name: 'Mei Lin Chen',
    role: 'Student Visa Client',
    avatar: TESTIMONIAL_4,
    quote: 'I was overwhelmed by the visa process until I found AlfaOverseas. Their team guided me step by step. Now I am studying abroad!',
  },
];

function Home() {
  return (
    <>
      <Navbar />
      <Hero bgImage={HERO_BG} />
      <Services />
      <ProcessSteps />
      <Stats />
      <Testimonials testimonials={TESTIMONIALS} />
      <CallToAction />
      <Footer />
    </>
  );
}

export default Home;
