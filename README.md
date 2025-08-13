# MoochSwitcher 🔄

🔄 Mooch Switch - Get the most out of your free-tier API keys with automatic switching on rate limits

A lightweight Python utility that automatically switches between multiple API keys when hitting rate limits, maximizing your usage of free-tier LLM APIs.

## ✨ Key Features

- **🔄 Automatic Switching**: Seamlessly switch between multiple API keys when rate limits are hit
- **🎯 Multi-Provider Support**: Works with OpenAI and LiteLLM (supporting 100+ LLM providers)
- **📊 Smart Retry Logic**: Intelligently retry with different keys on failures
- **🔧 Drop-in Replacement**: Minimal code changes required - just wrap your existing client
- **📝 Verbose Logging**: Optional detailed logging for debugging and monitoring
- **⚡ Lightweight**: Minimal dependencies, focused on core functionality

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/moochswitcher.git
cd moochswitcher

# Install dependencies
pip install -r requirements.txt
```

**Dependencies:**
- Python 3.7+
- litellm

### Basic Usage

```python
from mooch import mooch
import openai
import litellm

# Your API keys (can be string or list)
api_keys = [
    "sk-key1...",
    "sk-key2...",
    "sk-key3..."
]

# OpenAI Client Example
client = mooch(openai.OpenAI)(
    api_keys=api_keys,
    base_url="https://api.openai.com/v1"
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=100
)

# LiteLLM Example
completion = mooch(litellm.completion)(api_keys=api_keys)

response = completion(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=100
)
```

## 📖 Configuration

Create a `configs/config.yaml` file for easy management:

```yaml
openai:
  base_url: "https://api.openai.com/v1" # (Optional)
  api_keys:
    - "sk-key1..."
    - "sk-key2..."
  model: "gpt-3.5-turbo"

litellm:
  base_url: "https://XXX/v1" # (Optional)
  api_keys:
    - "sk-or-key1..."
    - "sk-or-key2..."
  model: "openrouter/qwen/qwen-2.5-coder-32b-instruct:free"
```

## 🔧 Advanced Usage

### Enable Verbose Logging

```python
# Enable verbose logging globally
mooch_verbose = mooch(verbose=True)
client = mooch_verbose(openai.OpenAI)(api_keys=api_keys)

# Or enable for specific calls
client = mooch(openai.OpenAI, verbose=True)(api_keys=api_keys)
```

### Error Handling

MoochSwitcher automatically handles:
- Rate limit errors (429)
- Authentication errors (401)
- Other API errors

If all keys fail, the last error is raised.

### Supported Providers

- **OpenAI**: Direct OpenAI API and compatible endpoints
- **LiteLLM**: 100+ providers including:
  - OpenRouter
  - Anthropic Claude
  - Google Gemini
  - Hugging Face
  - And many more...

## 🧪 Testing

```bash
# Run tests
python -m unittest mooch.test

# Or use pytest
python -m pytest mooch/test.py -v
```

## 📚 API Reference

### mooch Function

```python
mooch(target, verbose: bool = False)
```

**Parameters:**
- `target`: The client class or function to wrap (`openai.OpenAI` or `litellm.completion`)
- `verbose`: Enable detailed logging (default: False)

**Returns:**
- A wrapper function that accepts `api_keys` and other parameters

### Wrapper Functions

#### For OpenAI Client
```python
client = mooch(openai.OpenAI)(
    api_keys: Union[str, List[str]],
    *args,
    **kwargs  # Standard OpenAI client parameters
)
```

#### For LiteLLM Completion
```python
completion = mooch(litellm.completion)(
    api_keys: Union[str, List[str]]
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built for developers maximizing free-tier API usage
- Inspired by the need for seamless API key management
- Thanks to the LiteLLM project for multi-provider support

---

Made with ❤️ for the developer community 