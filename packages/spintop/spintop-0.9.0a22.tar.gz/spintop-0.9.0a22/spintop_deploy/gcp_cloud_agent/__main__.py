import os
import dotenv
dotenv.load_dotenv()

from .handler import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5080)))