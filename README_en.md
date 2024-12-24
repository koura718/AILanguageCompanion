# MyChatMe - Multilingual AI Chat Application

[![Built with Streamlit](https://img.shields.io/badge/built%20with-Streamlit-ff4b4b.svg)](https://www.streamlit.io)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced multilingual AI chat application designed to streamline cross-language communication and prompt template management.

[日本語](README.md) | English

## 🌟 Key Features

- 🤖 Multiple AI Model Support
  - OpenAI GPT-4
  - Google Gemini-2.0
  - Anthropic Claude-3.5
- 🌐 Multilingual Support
  - English and Japanese interfaces
  - Language switching capability
- 📝 Prompt Template Management
  - Save and edit templates
  - Category classification
- 💾 Chat History
  - Export as Markdown
  - PDF output support
- 🎨 Customizable Themes
- ⚡ Responsive Design

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.12
- **AI Integration**:
  - OpenAI API
  - Google Gemini API (via OpenRouter)
  - Anthropic Claude API (via OpenRouter)
- **Internationalization**: Custom i18n system
- **Data Export**: ReportLab (PDF generation)

## 📋 Prerequisites

- Python 3.12 or higher
- OpenAI API key
- OpenRouter API key (for Gemini-2.0 and Claude-3.5)

## 🚀 Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mychatme.git
cd mychatme
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
# Create .env file
OPENAI_API_KEY=your_openai_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

4. Start the application:
```bash
streamlit run main.py
```

## 💡 Usage

1. **Language Selection**:
   - Choose English/Japanese from the sidebar

2. **AI Model Selection**:
   - Choose between GPT-4, Gemini-2.0, and Claude-3.5
   - Select based on each model's strengths

3. **Prompt Templates**:
   - Create and save templates
   - Load saved templates
   - Edit and delete templates

4. **Chat History Management**:
   - Export chat content (MD/PDF)
   - Timezone-aware history management

5. **Theme Customization**:
   - Light/Dark mode
   - Color theme changes

## 🔒 Security

- API credentials managed via environment variables
- Secure session state management
- Error handling and rate limiting implementation

## 🤝 Contributing

1. Fork this repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Amazing web application framework
- [OpenAI](https://openai.com/) - GPT-4 model provider
- [OpenRouter](https://openrouter.ai/) - Unified AI model access
- [ReportLab](https://www.reportlab.com/) - PDF export functionality

## 📞 Support

If you have any issues or suggestions, please let us know in the GitHub Issues section.
