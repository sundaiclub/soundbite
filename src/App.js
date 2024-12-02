import React, { useState, useEffect } from "react";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import Modal from "react-modal";
import axios from "axios";
import { motion } from "framer-motion";
import { FaGoogle } from "react-icons/fa";
import {
  HiOutlineSparkles,
  HiOutlineMail,
  HiOutlinePlay,
} from "react-icons/hi";
import { RiTimeLine, RiRocketLine, RiFlowChart } from "react-icons/ri";
import { FiTwitter, FiInstagram, FiLinkedin } from "react-icons/fi";

// Initialize Modal
Modal.setAppElement("#root");

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:3001";

function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [accessToken, setAccessToken] = useState(null);
  const [authError, setAuthError] = useState(null);

  const handleGoogleSuccess = async (credentialResponse) => {
    console.log("Google Login Success Response:", credentialResponse);

    if (credentialResponse.credential) {
      try {
        // First, get the authorization URL
        // const authResponse = await axios.get(`${API_URL}/auth/google`);
        // console.log("Auth URL:", authResponse.data.url);

        // Store the credential
        setAccessToken(credentialResponse.credential);

        // Open the Google authorization window
        // window.location.href = authResponse.data.url;
      } catch (error) {
        console.error("Error starting OAuth flow:", error);
        setAuthError("Failed to start authentication process");
      }
    } else {
      console.error("No credential received");
      setAuthError("No authentication credential received");
    }
  };

  const handleEmailAccess = async () => {
    try {
      console.log("Attempting to authorize with token:", accessToken);

      const response = await axios.post(`${API_URL}/api/gmail/authorize`, {
        token: accessToken,
      });

      console.log("Email access response:", response.data);
      setIsModalOpen(false);
    } catch (error) {
      console.error("Error accessing emails:", error);
      setAuthError("Failed to access emails");
    }
  };

  // Add error display to your Modal
  const renderModal = () => (
    <Modal
      isOpen={isModalOpen}
      onRequestClose={() => setIsModalOpen(false)}
      className="modal-content"
      overlayClassName="modal-overlay"
    >
      <h2 className="text-xl font-bold mb-4">Email Access Permission</h2>
      {authError && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {authError}
        </div>
      )}
      <p className="mb-6">
        We need your permission to access your emails for analysis.
      </p>
      <div className="flex justify-end space-x-4">
        <button
          onClick={handleEmailAccess}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Grant Access
        </button>
        <button
          onClick={() => setIsModalOpen(false)}
          className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded"
        >
          Cancel
        </button>
      </div>
    </Modal>
  );

  return (
    <div className="min-h-screen bg-black">
      {/* Hero Section */}
      <section className="relative h-screen">
        <div
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: `url('https://images.unsplash.com/photo-1593697909777-138e8c90ac91?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')`,
          }}
        >
          <div className="absolute inset-0 hero-gradient" />
        </div>

        <div className="relative h-full flex flex-col items-center justify-center text-white px-4">
          <motion.img
            src={require("./assets/logo.png.png")}
            alt="Sound Bites Logo"
            className="w-64 md:w-96 mb-16"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8 }}
          />
          <motion.h1
            className="text-5xl md:text-7xl font-bold text-center mb-12 max-w-4xl"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            Your Substacks, in a 5-min podcast—delivered instantly.
          </motion.h1>

          <GoogleOAuthProvider
            redirectUrl="http://localhost:3000/"
            clientId="PUT CLIENT ID HERE"
          >
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={(error) => {
                console.error("Login Failed:", error);
                setAuthError(error.message || "Authentication failed");
              }}
              scope="https://www.googleapis.com/auth/gmail.readonly email profile"
              useOneTap
              flow="implicit"
              cookiePolicy={"single_host_origin"}
            />
            {renderModal()}
          </GoogleOAuthProvider>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-32 bg-black">
        <div className="container mx-auto px-4">
          <h2 className="section-title">How It Works</h2>

          <div className="grid md:grid-cols-3 gap-12 max-w-6xl mx-auto">
            {[
              {
                icon: <HiOutlineMail className="text-6xl text-red-600" />,
                title: "Hook Us Up",
                description:
                  "Link your Gmail, and we'll pull the best from the last 10 days of your Substack.",
              },
              {
                icon: <HiOutlineSparkles className="text-6xl text-red-600" />,
                title: "We Spill the Tea",
                description:
                  "Your updates, flipped into a 🔥 5-min podcast you'll actually want to hear.",
              },
              {
                icon: <HiOutlinePlay className="text-6xl text-red-600" />,
                title: "You Listen",
                description:
                  "Dropped instantly fresh, ready to play whenever you are.",
              },
            ].map((block, index) => (
              <motion.div
                key={index}
                className="feature-block"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.2 }}
                viewport={{ once: true }}
              >
                <div className="mb-8">{block.icon}</div>
                <h3 className="text-2xl font-bold mb-4 text-white">
                  {block.title}
                </h3>
                <p className="text-zinc-400 text-lg leading-relaxed">
                  {block.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Why Choose Section */}
      <section className="py-32 bg-zinc-950">
        <div className="container mx-auto px-4">
          <h2 className="section-title">Why Choose Sound Bites?</h2>

          <div className="grid md:grid-cols-3 gap-12 max-w-6xl mx-auto">
            {[
              {
                icon: <RiTimeLine className="text-6xl text-red-600" />,
                title: "No more FOMO",
                description:
                  "Stay in the Loop, get the highlights that actually matter.",
              },
              {
                icon: <RiRocketLine className="text-6xl text-red-600" />,
                title: "Escape inbox overload",
                description:
                  "Save Time, get only the best of your Substacks in minutes.",
              },
              {
                icon: <RiFlowChart className="text-6xl text-red-600" />,
                title: "Zero Effort",
                description:
                  "Seamlessly syncs with Google, delivered straight to your inbox.",
              },
            ].map((feature, index) => (
              <motion.div
                key={index}
                className="feature-block"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.2 }}
                viewport={{ once: true }}
              >
                <div className="mb-8">{feature.icon}</div>
                <h3 className="text-2xl font-bold mb-4 text-white">
                  {feature.title}
                </h3>
                <p className="text-zinc-400 text-lg leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-16 bg-black border-t border-zinc-900">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="space-x-8 mb-8 md:mb-0">
              <a href="#" className="nav-link">
                About
              </a>
              <a href="#" className="nav-link">
                Contact
              </a>
              <a href="#" className="nav-link">
                Privacy Policy
              </a>
            </div>

            <div className="flex space-x-6">
              {[FiTwitter, FiInstagram, FiLinkedin].map((Icon, index) => (
                <a
                  key={index}
                  href="#"
                  className="text-zinc-500 hover:text-red-600 transition-colors"
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
