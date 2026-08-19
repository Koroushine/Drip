"""
Drip AI Chatbot Server
Integrated with NCERT Science RAG System (Class 8, 9, 10)
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import json
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the src directory to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import the RAG modules
try:
    from src.tutor import AITutor
    from src.student_profile import StudentProfile
    from src.config import OPENROUTER_API_KEY, TEST_QUESTIONS, DATA_FOLDER, MODELS
    
    RAG_AVAILABLE = True
    logger.info("✅ RAG modules imported successfully")
except ImportError as e:
    RAG_AVAILABLE = False
    logger.warning(f"⚠️ RAG modules not available: {e}")
    logger.warning("⚠️ Running in simplified mode")

# Create Flask app
app = Flask(__name__, static_folder='../')
CORS(app)

# Initialize AITutor if available
tutor = None
if RAG_AVAILABLE:
    try:
        # Check API key
        if OPENROUTER_API_KEY and OPENROUTER_API_KEY not in ["your-openrouter-api-key-here", "your-key-here"]:
            tutor = AITutor(folder=DATA_FOLDER, api_key=OPENROUTER_API_KEY)
            logger.info("✅ AITutor initialized successfully with API key")
        else:
            logger.warning("⚠️ OPENROUTER_API_KEY not set in .env file")
            logger.warning("⚠️ AITutor will work in fallback mode (knowledge base only)")
            # Still initialize without API key (will use knowledge base)
            tutor = AITutor(folder=DATA_FOLDER)
            logger.info("✅ AITutor initialized (fallback mode)")
    except Exception as e:
        logger.error(f"❌ Failed to initialize AITutor: {e}")
        RAG_AVAILABLE = False

# Simple knowledge base (fallback)
KNOWLEDGE_BASE = {
    'photosynthesis': '🌿 Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to create oxygen and energy in the form of sugar.',
    'newton': "⚡ Newton's three laws of motion:\n1. Inertia: Objects stay at rest or in motion unless acted upon\n2. F = ma (Force = mass × acceleration)\n3. Action-Reaction: For every action, there is an equal and opposite reaction",
    'acid': '🧪 An acid is a substance that donates hydrogen ions (H+) in aqueous solution. Acids have a pH less than 7.',
    'cell': '🧬 Cells are the basic building blocks of all living things. They provide structure, take in nutrients, and carry out important functions.',
    'force': '💪 Force is a push or pull that can change the motion of an object. Measured in Newtons (N).',
    'friction': '🔧 Friction is a force that opposes motion between two surfaces in contact.',
    'light': '💡 Light is electromagnetic radiation visible to the human eye. Speed: 299,792,458 m/s.',
    'sound': '🔊 Sound is a vibration that travels through a medium (air, water, solids) as waves.',
    'biology': '🧬 Biology is the study of living organisms and their interactions with the environment.',
    'chemistry': '🧪 Chemistry is the study of matter, its properties, composition, and changes.',
    'physics': '⚡ Physics is the study of matter, energy, and their interactions.',
    'electricity': '⚡ Electricity is the flow of electric charge. It powers our homes and devices. Key concepts: current, voltage, resistance, Ohm\'s law.',
    'magnet': '🧲 Magnetism is a force that attracts or repels certain materials. Electromagnets are used in motors and generators.',
    'atom': '⚛️ Atoms are the basic building blocks of matter. They consist of protons, neutrons, and electrons.',
    'compound': '🧪 A compound is a substance made of two or more elements chemically bonded together.',
    'element': '🔬 An element is a pure substance that cannot be broken down into simpler substances.',
    'reproduction': '🌱 Reproduction is the biological process by which new individual organisms are produced.',
    'heredity': '🧬 Heredity is the passing of traits from parents to offspring through genes.',
    'ecosystem': '🌍 An ecosystem is a community of living organisms interacting with their non-living environment.',
}

# ============================================================
# Routes
# ============================================================

@app.route('/')
def index():
    """Serve the chatbot page"""
    return send_from_directory('../', 'chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests using the AITutor"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        student_id = data.get('student_id', 'default')
        
        if not message:
            return jsonify({
                'response': 'Please ask me a question about science!',
                'success': True
            })
        
        logger.info(f"📨 Received message from {student_id}: {message[:50]}...")
        
        # Use RAG if available
        if RAG_AVAILABLE and tutor:
            try:
                # Get student profile
                student = tutor.get_student(student_id)
                
                # Use the tutor to explain
                result = tutor.explain(
                    concept=message,
                    student_id=student_id
                )
                
                if result and result.get('explanation') and not result.get('error'):
                    response = result['explanation']
                    
                    # Add follow-up if available
                    if result.get('follow_up'):
                        response += f"\n\n💡 Follow-up: {result['follow_up']}"
                    
                    # Add source info
                    if result.get('sources'):
                        sources = ', '.join(result['sources'][:2])
                        response += f"\n\n📚 Sources: {sources}"
                    
                    logger.info(f"✅ RAG response generated")
                    
                    return jsonify({
                        'response': response,
                        'success': True,
                        'source': 'rag',
                        'level': result.get('level', 'moderate'),
                        'grade': result.get('grade', 'Class 9')
                    })
                else:
                    # Fall back to knowledge base
                    return fallback_response(message)
                    
            except Exception as e:
                logger.error(f"❌ RAG error: {e}")
                # Fall back to simple mode
                return fallback_response(message)
        else:
            # Use simple knowledge base
            return fallback_response(message)
            
    except Exception as e:
        logger.error(f"❌ Chat error: {e}")
        return jsonify({
            'response': f"⚠️ I encountered an error: {str(e)}",
            'success': False,
            'error': str(e)
        }), 500

def fallback_response(message):
    """Simple knowledge base response (fallback)"""
    message_lower = message.lower()
    
    # Check for specific keywords
    for key, value in KNOWLEDGE_BASE.items():
        if key in message_lower:
            return jsonify({
                'response': value + "\n\n📚 Is there anything else you'd like to know about this topic?",
                'success': True,
                'source': 'fallback'
            })
    
    # Check for broader topics
    if any(word in message_lower for word in ['physics', 'force', 'energy', 'motion', 'gravity']):
        response = "⚡ Physics topics I can help with:\n• Force & Pressure\n• Friction\n• Light & Optics\n• Sound\n• Electricity & Magnetism\n• Solar System\n\nWhat specific physics topic would you like to learn about?"
    elif any(word in message_lower for word in ['chemistry', 'acid', 'base', 'metal', 'compound', 'reaction']):
        response = "🧪 Chemistry topics I can help with:\n• Acids, Bases & Salts\n• Metals & Non-metals\n• Chemical Reactions\n• Carbon & its Compounds\n• Synthetic Fibres\n• Materials\n\nAsk me about any of these!"
    elif any(word in message_lower for word in ['biology', 'cell', 'body', 'plant', 'animal', 'ecosystem', 'gene']):
        response = "🧬 Biology topics I can help with:\n• Cell Structure & Function\n• Microorganisms\n• Human Body Systems\n• Plants & Photosynthesis\n• Ecosystems & Food Chains\n• Genetics & Heredity\n\nWhat would you like to explore?"
    else:
        response = "🤖 I'm your AI Science Tutor! I can help you with:\n\n🔬 **Physics**: Force, Light, Sound, Electricity, Friction\n🧪 **Chemistry**: Acids, Metals, Reactions, Compounds\n🧬 **Biology**: Cells, Human Body, Plants, Ecosystems\n\nWhat would you like to learn about today? Just ask me any science question!"
    
    return jsonify({
        'response': response,
        'success': True,
        'source': 'fallback'
    })

@app.route('/api/hint', methods=['POST'])
def get_hint():
    """Get a progressive hint for a question"""
    try:
        data = request.json
        question = data.get('question', '')
        student_id = data.get('student_id', 'default')
        
        if RAG_AVAILABLE and tutor:
            try:
                result = tutor.hint(question, student_id)
                return jsonify({
                    'hint': result.get('hint', 'Think about what you know from NCERT.'),
                    'level': result.get('level', 'moderate'),
                    'success': True
                })
            except Exception as e:
                logger.error(f"❌ Hint error: {e}")
                return jsonify({
                    'hint': 'Try breaking down the question into smaller parts. What do you already know?',
                    'success': True
                })
        else:
            return jsonify({
                'hint': 'Try to recall what you learned in class. Look for keywords in the question.',
                'success': True
            })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/quiz', methods=['POST'])
def generate_quiz():
    """Generate a quiz on a topic"""
    try:
        data = request.json
        topic = data.get('topic', '')
        num_questions = data.get('num_questions', 3)
        difficulty = data.get('difficulty', 1)
        student_id = data.get('student_id', 'default')
        
        if RAG_AVAILABLE and tutor:
            try:
                result = tutor.quiz(topic, num_questions, difficulty, student_id)
                return jsonify({
                    'quiz': result.get('quiz', ''),
                    'topic': topic,
                    'difficulty': result.get('difficulty', 'Moderate'),
                    'success': True
                })
            except Exception as e:
                logger.error(f"❌ Quiz error: {e}")
                return jsonify({
                    'quiz': f"Here are some questions about '{topic}':\n\n1. What do you know about {topic}?\n2. Can you give an example of {topic}?\n3. Why is {topic} important?",
                    'success': True
                })
        else:
            return jsonify({
                'quiz': f"Here are some questions about '{topic}':\n\n1. What is {topic}?\n2. How does {topic} work?\n3. Can you think of a real-world example of {topic}?",
                'success': True
            })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get student progress"""
    try:
        student_id = request.args.get('student_id', 'default')
        
        if RAG_AVAILABLE and tutor:
            try:
                summary = tutor.progress(student_id)
                return jsonify({
                    'progress': summary,
                    'success': True
                })
            except Exception as e:
                logger.error(f"❌ Progress error: {e}")
                return jsonify({
                    'progress': {
                        'weak_topics': [],
                        'mastered_topics': ['Getting started...'],
                        'average_score': 0,
                        'total_quizzes': 0,
                        'total_questions': 0
                    },
                    'success': True
                })
        else:
            return jsonify({
                'progress': {
                    'weak_topics': ['Loading...'],
                    'mastered_topics': ['Start learning to build mastery!'],
                    'average_score': 0,
                    'total_quizzes': 0,
                    'total_questions': 0,
                    'recommendations': {'message': 'Ask me a question to start learning!'}
                },
                'success': True
            })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/recommend', methods=['GET'])
def get_recommendations():
    """Get personalized recommendations"""
    try:
        student_id = request.args.get('student_id', 'default')
        
        if RAG_AVAILABLE and tutor:
            try:
                recommendations = tutor.recommend(student_id)
                return jsonify({
                    'recommendations': recommendations,
                    'success': True
                })
            except Exception as e:
                logger.error(f"❌ Recommendations error: {e}")
                return jsonify({
                    'recommendations': {'message': 'Keep learning and exploring science!'},
                    'success': True
                })
        else:
            return jsonify({
                'recommendations': {
                    'message': 'Ask me questions to get personalized learning recommendations!',
                    'focus_on': ['Start with any topic you find interesting']
                },
                'success': True
            })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/knowledge/search', methods=['POST'])
def search_knowledge():
    """Search the knowledge base"""
    try:
        data = request.json
        query = data.get('query', '')
        grade = data.get('grade', None)
        limit = data.get('limit', 5)
        
        if RAG_AVAILABLE and tutor:
            try:
                # Use the knowledge base search
                results = tutor.knowledge.search(query, grade=grade, top_k=limit)
                return jsonify({
                    'results': results,
                    'success': True,
                    'source': 'rag'
                })
            except Exception as e:
                logger.error(f"❌ Search error: {e}")
        
        # Fallback search
        results = []
        for key, value in KNOWLEDGE_BASE.items():
            if query.lower() in key.lower() or any(word in value.lower() for word in query.lower().split()):
                results.append({
                    'text': value,
                    'score': 1.0,
                    'metadata': {'topic': key, 'grade': 'Unknown'}
                })
        
        return jsonify({
            'results': results[:limit],
            'success': True,
            'source': 'fallback'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    status = {
        'status': 'healthy',
        'rag_available': RAG_AVAILABLE,
        'tutor_initialized': tutor is not None,
        'server': 'Drip AI Chatbot',
        'version': '2.0.0'
    }
    
    if tutor:
        try:
            stats = tutor.knowledge.get_stats()
            status['knowledge_stats'] = stats
        except:
            pass
    
    return jsonify(status)

@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Get available topics"""
    try:
        if RAG_AVAILABLE and tutor:
            try:
                # Extract topics from knowledge base
                topics = set()
                for meta in tutor.knowledge.metadata:
                    for topic in meta.get('topics', []):
                        topics.add(topic)
                return jsonify({
                    'topics': sorted(list(topics)),
                    'success': True
                })
            except:
                pass
        
        # Fallback topics
        return jsonify({
            'topics': sorted(list(KNOWLEDGE_BASE.keys())),
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('../', path)

# ============================================================
# Main Entry Point
# ============================================================

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 DRIP AI CHATBOT SERVER")
    print("=" * 70)
    print(f"📍 RAG System: {'✅ AVAILABLE' if RAG_AVAILABLE else '⚠️ FALLBACK MODE'}")
    print(f"📍 Tutor: {'✅ INITIALIZED' if tutor else '❌ NOT INITIALIZED'}")
    
    # Check API key status
    api_key_status = '⚠️ NOT SET'
    if OPENROUTER_API_KEY:
        if OPENROUTER_API_KEY not in ['your-openrouter-api-key-here', 'your-key-here']:
            api_key_status = '✅ SET'
    print(f"📍 API Key: {api_key_status}")
    
    print(f"📍 Server URL: http://localhost:5000")
    print(f"📍 Chatbot URL: http://localhost:5000")
    print("=" * 70)
    
    if RAG_AVAILABLE and tutor:
        try:
            stats = tutor.knowledge.get_stats()
            print(f"📚 Knowledge Base Stats:")
            print(f"   • Total chunks: {stats.get('total_chunks', 0)}")
            print(f"   • Files loaded: {stats.get('loaded_files', 0)}")
            grade_counts = stats.get('grade_counts', {})
            if grade_counts:
                print(f"   • Class 8: {grade_counts.get('Class 8', 0)} chunks")
                print(f"   • Class 9: {grade_counts.get('Class 9', 0)} chunks")
                print(f"   • Class 10: {grade_counts.get('Class 10', 0)} chunks")
        except Exception as e:
            print(f"⚠️ Could not get stats: {e}")
    else:
        print("📚 Running in fallback mode with built-in knowledge base")
        print(f"   • Available topics: {len(KNOWLEDGE_BASE)}")
    
    print("=" * 70)
    print("💡 Tips:")
    print("   • Try asking: 'What is photosynthesis?'")
    print("   • Try asking: 'Explain Newton's laws'")
    print("   • Try asking: 'What is an acid?'")
    print("   • Try asking: 'How does electricity work?'")
    print("=" * 70)
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)