import { useState, useEffect } from 'react'
import PaymentButton from './components/PaymentButton'
import './App.css'

function App() {
  const [isPaid, setIsPaid] = useState(false)
  const [selectedCard, setSelectedCard] = useState(null)
  const [isFlipped, setIsFlipped] = useState(false)

  // Cargar cartas del JSON
  const loadCard = async () => {
    try {
      // Cargar uno de los archivos JSON de cartas
      const response = await fetch('/data/0-5.json')
      const cards = await response.json()
      
      // Seleccionar una carta aleatoria
      const randomCard = cards[Math.floor(Math.random() * cards.length)]
      setSelectedCard(randomCard)
    } catch (error) {
      console.error('Error cargando carta:', error)
    }
  }

  useEffect(() => {
    // Cargar una carta al iniciar
    loadCard()
  }, [])

  const handlePaymentSuccess = () => {
    setIsPaid(true)
    // Revelar la carta después del pago
    setTimeout(() => {
      setIsFlipped(true)
    }, 300)
  }

  const handleReset = () => {
    setIsPaid(false)
    setIsFlipped(false)
    loadCard()
  }

  return (
    <div className="app">
      <div className="wallpaper">
        <div className="blob blob1"></div>
        <div className="blob blob2"></div>
        <div className="blob blob3"></div>
        <div className="blob blob4"></div>
      </div>
      <div className="noise-overlay"></div>

      <div className="interface">
        <h1 className="title">Star ✦</h1>
        
        <div className={`card-stage ${isFlipped ? 'flipped' : ''}`}>
          <div className="card-inner">
            <div className="card-face front">
              <div className="symbol">☾</div>
            </div>
            <div className="card-face back">
              {selectedCard && (
                <img 
                  src={`/cards/ar${String(selectedCard.id).padStart(2, '0')}.jpg`} 
                  alt={selectedCard.nombre}
                  className="tarot-img"
                />
              )}
            </div>
          </div>
        </div>

        {!isPaid && !isFlipped && (
          <div className="payment-section">
            <p className="instruction">Realiza el pago para revelar tu carta</p>
            <PaymentButton onPaymentSuccess={handlePaymentSuccess} />
          </div>
        )}

        {isPaid && isFlipped && selectedCard && (
          <div className="insight-panel active">
            <h2>{selectedCard.nombre}</h2>
            
            <div className="section">
              <div className="section-title">✧ Sombras y Peligros</div>
              <p className="section-content">{selectedCard.contenido.sombra}</p>
            </div>

            <div className="section">
              <div className="section-title">✦ Misticismo</div>
              <p className="section-content">{selectedCard.contenido.misticismo}</p>
            </div>

            <div className="section">
              <div className="section-title">✧ Arquetipo</div>
              <p className="section-content">{selectedCard.contenido.arquetipo}</p>
            </div>

            {selectedCard.contenido.botanica && (
              <div className="section">
                <div className="section-title">✦ Botánica</div>
                <p className="section-content">{selectedCard.contenido.botanica}</p>
              </div>
            )}

            {selectedCard.contenido.cotidiano && (
              <div className="section">
                <div className="section-title">✧ Cotidiano</div>
                <p className="section-content">{selectedCard.contenido.cotidiano}</p>
              </div>
            )}

            {selectedCard.contenido.gnosis && (
              <div className="section">
                <div className="section-title">✦ Gnosis</div>
                <p className="section-content">{selectedCard.contenido.gnosis}</p>
              </div>
            )}

            {selectedCard.contenido.resonancia_biblica && (
              <div className="section">
                <div className="section-title">✧ Resonancia Bíblica</div>
                <div className="biblical-verse">
                  "{selectedCard.contenido.resonancia_biblica.cita}"
                  <span className="verse-reference">— {selectedCard.contenido.resonancia_biblica.referencia}</span>
                </div>
              </div>
            )}

            <button 
              className="reset-button" 
              onClick={handleReset}
            >
              Nueva Consulta
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
