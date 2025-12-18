from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.error

class handler(BaseHTTPRequestHandler):
    """
    Server-side World ID verification endpoint.
    This is REQUIRED by Worldcoin to prevent client-side only verification.
    """
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def _set_cors_headers(self):
        """Set CORS headers for cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_POST(self):
        """Verify World ID proof on server-side"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            # Extract verification data
            proof = data.get('proof')
            merkle_root = data.get('merkle_root')
            nullifier_hash = data.get('nullifier_hash')
            action = data.get('action', 'star-oracle-verification')
            signal = data.get('signal', '')
            
            if not proof or not merkle_root or not nullifier_hash:
                self.send_response(400)
                self._set_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': 'Missing required fields: proof, merkle_root, nullifier_hash'
                }).encode('utf-8'))
                return
            
            # Call Worldcoin verification API
            verify_url = 'https://developer.worldcoin.org/api/v1/verify'
            
            verify_payload = {
                'proof': proof,
                'merkle_root': merkle_root,
                'nullifier_hash': nullifier_hash,
                'action': action,
                'signal': signal
            }
            
            # Make request to Worldcoin API
            req = urllib.request.Request(
                verify_url,
                data=json.dumps(verify_payload).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                }
            )
            
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    response_data = json.loads(response.read().decode('utf-8'))
                    
                    # Check if verification was successful
                    if response_data.get('success'):
                        self.send_response(200)
                        self._set_cors_headers()
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            'success': True,
                            'verified': True,
                            'nullifier_hash': nullifier_hash
                        }).encode('utf-8'))
                    else:
                        self.send_response(400)
                        self._set_cors_headers()
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            'success': False,
                            'verified': False,
                            'error': response_data.get('detail', 'Verification failed')
                        }).encode('utf-8'))
                        
            except urllib.error.HTTPError as e:
                error_body = e.read().decode('utf-8')
                print(f"Worldcoin API error: {e.code} - {error_body}")
                
                self.send_response(400)
                self._set_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'verified': False,
                    'error': f'Worldcoin API error: {e.code}'
                }).encode('utf-8'))
                
        except Exception as e:
            print(f"Verification error: {str(e)}")
            self.send_response(500)
            self._set_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e)
            }).encode('utf-8'))
    
    def do_GET(self):
        """Health check endpoint"""
        self.send_response(200)
        self._set_cors_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'status': 'active',
            'service': 'World ID Verification',
            'endpoint': '/api/verify_world_id'
        }).encode('utf-8'))
