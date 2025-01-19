import os
from dotenv import load_dotenv
import uvicorn
from poet.api import app

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '8000'))
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=debug
    )
