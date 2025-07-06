/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
      },
      colors: {
        // Zanvar Group Brand Colors
        'zanvar': {
          'primary': '#1e3a8a',     // Deep blue
          'secondary': '#3b82f6',   // Bright blue  
          'accent': '#f59e0b',      // Golden amber
          'dark': '#1e293b',       // Dark slate
          'light': '#f8fafc',      // Light gray
        },
        'chat-bg': '#f8fafc',
        'user-msg': '#1e3a8a',
        'bot-msg': '#ffffff',
        'sidebar': '#1e293b',
        'input-bg': '#334155',
        'accent-gold': '#f59e0b',
        'text-muted': '#64748b',
      },
      backgroundImage: {
        'gradient-zanvar': 'linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)',
        'gradient-gold': 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
      },
      boxShadow: {
        'zanvar': '0 10px 25px -3px rgba(30, 58, 138, 0.1), 0 4px 6px -2px rgba(30, 58, 138, 0.05)',
        'chat': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      }
    },
  },
  plugins: [],
}
