// tailwind.config.js
import defaultTheme from 'tailwindcss/defaultTheme'

export default {
  // Le dice a Tailwind qué archivos escanear
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./src/assets/main.css",
  ],
  
  theme: {
    // 'extend' añade tus estilos a los de Tailwind,
    // en lugar de reemplazarlos.
    extend: {
      colors: {
        // (Aquí puedes poner tu rojo para usar 'bg-brand-red')
        'brand-red': '#dc2626', 
      },
      
      fontFamily: {
        // Esto crea la clase 'font-display'
        'display': ['"Antonio"', ...defaultTheme.fontFamily.sans],
        
        // Esto crea la clase 'font-space'
        'space': ['"Space Mono"', ...defaultTheme.fontFamily.mono],
      }
    }
  },
  
  plugins: [],
}