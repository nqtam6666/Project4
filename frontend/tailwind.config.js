/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{html,js}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: 'var(--bg-page)',
        surface: 'var(--bg-surface)',
        'surface-container-lowest': 'var(--bg-sidebar)',
        'surface-container-low': 'var(--bg-surface-low)',
        'surface-container': 'var(--bg-surface)',
        'surface-container-high': 'var(--bg-surface-high)',
        'surface-container-highest': 'var(--bg-surface-highest)',
        'surface-variant': 'var(--bg-surface-highest)',
        'surface-bright': 'var(--bg-surface-high)', // approx
        'on-surface': 'var(--text-main)',
        'on-surface-variant': 'var(--text-secondary)',
        outline: 'var(--text-muted)',
        'outline-variant': 'var(--border-muted)',
        primary: 'var(--primary-color)',
        'primary-container': 'rgba(206,59,59,0.1)', 
        secondary: 'var(--secondary-color)',
        'secondary-container': 'rgba(81,139,189,0.1)',
        tertiary: 'var(--accent-orange)',
        'tertiary-container': '#df7412',
        error: 'var(--accent-red)',
        'error-container': '#93000a',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Inter', 'system-ui', 'sans-serif'],
        caps: ['Lexend', 'sans-serif'],
      },
      fontSize: {
        'display-xl': ['36px', { lineHeight: '1.2', letterSpacing: '-0.02em', fontWeight: '800' }],
        'headline-lg': ['24px', { lineHeight: '1.3', letterSpacing: '-0.01em', fontWeight: '700' }],
        'headline-md': ['20px', { lineHeight: '1.4', fontWeight: '600' }],
        'body-base': ['16px', { lineHeight: '1.6', fontWeight: '400' }],
        'body-sm': ['14px', { lineHeight: '1.5', fontWeight: '400' }],
        'label-caps': ['12px', { lineHeight: '1', letterSpacing: '0.05em', fontWeight: '600' }],
      },
      spacing: {
        xs: '4px',
        base: '4px',
        sm: '8px',
        md: '16px',
        lg: '24px',
        gutter: '20px',
        xl: '32px',
        margin: '40px',
      },
      borderRadius: {
        DEFAULT: '2px',
        lg: '4px',
        xl: '8px',
        full: '12px', // wait, rounded-full is usually 9999px. Style guide says "Pill badge" 12px. Let's make it 9999px and 12px for something else?
        // Ah, style guide literally says "rounded-full: 12px | Pill badge". I'll follow it.
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries')
  ],
};
