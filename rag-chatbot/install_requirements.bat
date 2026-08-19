@echo off
echo Installing Drip AI Chatbot Dependencies...
echo.

echo Installing numpy (pre-built)...
pip install --only-binary :all: numpy==1.26.4

echo Installing pandas (pre-built)...
pip install --only-binary :all: pandas==2.2.0

echo Installing scikit-learn (pre-built)...
pip install --only-binary :all: scikit-learn==1.3.0

echo Installing remaining packages...
pip install pypdf2==3.0.1
pip install chromadb==0.4.24
pip install langchain==0.1.16
pip install langchain-community==0.1.10
pip install flask==3.0.2
pip install flask-cors==4.0.1
pip install openai==1.12.0
pip install tiktoken==0.6.0
pip install sentence-transformers==2.3.1
pip install faiss-cpu==1.7.4
pip install python-dotenv==1.0.1

echo.
echo Installation complete!
pause