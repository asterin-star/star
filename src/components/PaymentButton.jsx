import React, { useState } from 'react';
import { MiniKit } from '@worldcoin/minikit-js';

const PaymentButton = ({ onPaymentSuccess }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handlePayment = async () => {
    if (!MiniKit.isInstalled()) {
      alert('Por favor, abre esta app en World App.');
      return;
    }

    setIsLoading(true);

    try {
      const payload = {
        reference: `tarot_${Date.now()}`,
        to: '0x0000000000000000000000000000000000000000', // PLACEHOLDER - El usuario debe reemplazar esto
        tokens: [
          {
            symbol: 'WLD',
            token_amount: '0.1', // 0.1 WLD por lectura
          }
        ],
        description: 'Lectura de Tarot - Una carta',
      };

      const { finalPayload } = await MiniKit.commandsAsync.pay(payload);

      if (finalPayload.status === 'success') {
        console.log('Pago exitoso!', finalPayload);
        onPaymentSuccess();
      } else {
        alert('El pago no se completó.');
      }
    } catch (error) {
      console.error('Error al procesar el pago:', error);
      alert('Ocurrió un error al intentar pagar.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button 
      onClick={handlePayment} 
      disabled={isLoading}
      style={{
        padding: '15px 30px',
        fontSize: '18px',
        backgroundColor: isLoading ? '#cccccc' : '#000000',
        color: 'white',
        border: 'none',
        borderRadius: '8px',
        cursor: isLoading ? 'not-allowed' : 'pointer',
        marginTop: '20px',
      }}
    >
      {isLoading ? 'Procesando...' : '🔮 Comprar Carta (0.1 WLD)'}
    </button>
  );
};

export default PaymentButton;
