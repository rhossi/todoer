/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        charcoal: '#0E1118',
        'charcoal-soft': '#181C25',
        'charcoal-muted': '#1F242F',
        'dash-green': '#A9FF5B',
        'dash-green-strong': '#7DFF32',
        'dash-orange': '#FF8B2C',
        'dash-orange-soft': '#FFA95B',
        'dash-cream': '#F9F7F1',
        'dash-gray': '#A0A3AD',
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'Inter', 'sans-serif'],
      },
      borderRadius: {
        '4xl': '2.5rem',
      },
      boxShadow: {
        glow: '0 15px 60px rgba(0, 0, 0, 0.45)',
        card: '0 20px 45px rgba(0, 0, 0, 0.55)',
      },
      backgroundImage: {
        'app-gradient':
          'radial-gradient(circle at 20% 20%, rgba(169,255,91,0.25), transparent 55%), radial-gradient(circle at 80% 0%, rgba(255,139,44,0.18), transparent 45%)',
      },
      spacing: {
        13: '3.25rem',
      },
    },
  },
  plugins: [],
}

