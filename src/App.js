import React from 'react';
import { motion } from 'framer-motion';
import { FaGoogle, FaInstagram, FaTwitter, FaLinkedin } from 'react-icons/fa';
import { MdEmail, MdNotifications } from 'react-icons/md';
import { BiLinkAlt } from 'react-icons/bi';
import { BsHeadphones } from 'react-icons/bs';

function App() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative h-screen">
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: `url('https://images.unsplash.com/photo-1593697909777-138e8c90ac91?q=80&w=2070&auto=format&fit=crop')`
          }}
        >
          <div className="absolute inset-0 hero-gradient" />
        </div>
        
        <div className="relative h-full flex flex-col items-center justify-center text-white px-4">
          <motion.h1 
            className="text-4xl md:text-6xl font-bold text-center mb-8 max-w-4xl"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            Your Substacks, in a fire 5-min podcast—delivered instantly.
          </motion.h1>
          
          <motion.button
            className="btn-primary flex items-center space-x-2"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <FaGoogle className="text-xl" />
            <span>Sign in with Google</span>
          </motion.button>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="section-title">How It Works</h2>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
              {
                icon: <BiLinkAlt className="text-4xl text-primary" />,
                title: "Hook Us Up",
                description: "Link your Gmail, and we'll pull the best from the last 10 days of your Substack."
              },
              {
                icon: <MdEmail className="text-4xl text-primary" />,
                title: "We Spill the Tea",
                description: "Your updates, flipped into a fire 5-min podcast you'll actually want to hear."
              },
              {
                icon: <BsHeadphones className="text-4xl text-primary" />,
                title: "You Listen",
                description: "Dropped instantly fresh, ready to play whenever you are."
              }
            ].map((block, index) => (
              <motion.div
                key={index}
                className="feature-block"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.2 }}
                viewport={{ once: true }}
              >
                <div className="mb-4">{block.icon}</div>
                <h3 className="text-xl font-bold mb-2">{block.title}</h3>
                <p className="text-gray-600">{block.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Why Choose Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="section-title">Why Choose Sound Bites?</h2>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
              {
                icon: <MdNotifications className="text-4xl text-accent" />,
                title: "No more FOMO",
                description: "Stay in the Loop, get the highlights that actually matter."
              },
              {
                icon: <MdEmail className="text-4xl text-accent" />,
                title: "Escape inbox overload",
                description: "Save Time, get only the best of your Substacks in minutes."
              },
              {
                icon: <FaGoogle className="text-4xl text-accent" />,
                title: "Zero Effort",
                description: "Seamlessly syncs with Google, delivered straight to your inbox."
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                className="feature-block"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.2 }}
                viewport={{ once: true }}
              >
                <div className="mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-dark text-white py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="space-x-6 mb-4 md:mb-0">
              <a href="#" className="hover:text-primary transition-colors">About</a>
              <a href="#" className="hover:text-primary transition-colors">Contact</a>
              <a href="#" className="hover:text-primary transition-colors">Privacy Policy</a>
            </div>
            
            <div className="flex space-x-4">
              {[FaInstagram, FaTwitter, FaLinkedin].map((Icon, index) => (
                <a
                  key={index}
                  href="#"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <Icon className="text-2xl" />
                </a>
              ))}
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
