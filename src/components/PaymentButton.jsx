import { MiniKit } from '@worldcoin/minikit-js'

export default function PaymentButton({ onSuccess }) {
  const handlePayment = async () => {
    if (!MiniKit.isInstalled()) {
      return
    }

    const res = await MiniKit.commandsAsync.pay({
      reference: `tarot-reading-${Date.now()}`,
      to: '0xa3cdea9fe705bc16dcd9e9170e217b0f1ba5aaf6',
      tokens: [
        {
          symbol: 'WLD',
          token_amount: '1.11',
        },
      ],
      description: 'Revelar carta del Tarot',
    })

    if (res.finalPayload.status === 'success') {
      const response = res.finalPayload;
      console.log('Payment successful!', response);
      
      if (onSuccess) {
        onSuccess(response);
      }
    } else {
      console.log('Payment failed', res.finalPayload);
    }
  }

  return (
    <button 
      onClick={handlePayment}
      className="payment-button"
    >
      Revelar carta · 1.11 WLD
    </button>
  )
}
