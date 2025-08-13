import openai
import litellm
from typing import List, Union, Callable


class MoochSwitcher:

    def __init__(self, verbose: bool = False):
        """
        Initialize MoochSwitcher
        
        Args:
            verbose: Default verbose setting
        """
        self.default_verbose = verbose

    def __call__(self, target, verbose: bool = None):
        """
        Wrap OpenAI client class or LiteLLM functions
        
        Args:
            target: The target to wrap (openai.OpenAI or litellm.completion)
            verbose: Whether to print switching logs (overrides default)
        """
        # Use provided verbose or fall back to default
        use_verbose = verbose if verbose is not None else self.default_verbose
        
        # If target is OpenAI class, return enhanced OpenAI class
        if target == openai.OpenAI:
            return lambda api_keys, *args, **kwargs: MoochForOpenAIClient(api_keys, use_verbose, *args, **kwargs)
        
        # If target is LiteLLM completion function, return enhanced LiteLLM class
        elif target == litellm.completion:
            return lambda api_keys: MoochForLiteLLMCompletion(api_keys, use_verbose)
        
        else:
            raise ValueError(f"Unsupported target: {target}")
    
    def _execute(self, api_keys: Union[str, List[str]], call_func: Callable, verbose: bool = False):
        """Common switching logic for both OpenAI and LiteLLM"""
        if isinstance(api_keys, str):
            api_keys = [api_keys]

        last_error = None
        
        for i, api_key in enumerate(api_keys):
            try:
                if verbose:
                    print()
                    print(f"[Mooch] Trying API key {i+1}/{len(api_keys)}: {api_key[:10]}...")
                
                result = call_func(api_key)
                
                if verbose:
                    print(f"[Mooch] ✓ Success with API key {i+1}")
                
                return result
                
            except openai.RateLimitError as e:
                if verbose:
                    print(f"[Mooch] ✗ Rate limit hit with API key {i+1}, switching...")
                last_error = e
                continue
        
        # All API keys failed
        if verbose:
            print(f"[Mooch] ✗ All {len(api_keys)} API keys failed")
        raise last_error


class MoochForOpenAIClient(openai.OpenAI):
    """Enhanced OpenAI client that switches API keys on rate limit errors"""
    
    def __init__(self, api_keys: List[str], verbose: bool = False, *args, **kwargs):
        self.api_keys = api_keys
        self.verbose = verbose
        self.switcher = MoochSwitcher(verbose)
        self.init_args = args
        self.init_kwargs = kwargs
        
        # Initialize with first API key
        super().__init__(api_key=api_keys[0], *args, **kwargs)
        
        # Override the chat.completions.create method
        self.chat.completions.create = self._create
    
    def _create(self, *args, **kwargs):
        """Create chat completion with API key switching"""
        return self.switcher._execute(
            self.api_keys,
            lambda api_key: self._call(api_key, *args, **kwargs),
            verbose=self.verbose
        )
    
    def _call(self, api_key, *args, **kwargs):
        """Call OpenAI with specific API key"""
        temp_client = openai.OpenAI(api_key=api_key, *self.init_args, **self.init_kwargs)
        return temp_client.chat.completions.create(*args, **kwargs)


class MoochForLiteLLMCompletion:
    """Enhanced LiteLLM completion that switches API keys on rate limit errors"""
    
    def __init__(self, api_keys: List[str], verbose: bool = False):
        self.api_keys = api_keys
        self.verbose = verbose
        self.switcher = MoochSwitcher(verbose)
    
    def __call__(self, *args, **kwargs):
        """Call LiteLLM completion with API key switching"""
        return self.switcher._execute(
            self.api_keys,
            lambda api_key: self._call(api_key, *args, **kwargs),
            verbose=self.verbose
        )
    
    def _call(self, api_key, *args, **kwargs):
        """Call LiteLLM function with specific API key"""
        kwargs['api_key'] = api_key
        return litellm.completion(*args, **kwargs)


# Global mooch switcher instance
mooch = MoochSwitcher()


if __name__ == "__main__":
    import os
    
    if not os.path.exists('configs/config.yaml'):
        print("config.yaml does not exist")
        exit(1)
    
    import yaml
    with open('configs/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Handle both str and list for api_key
    def get_keys(key_config):
        return [key_config] if isinstance(key_config, str) else key_config
    
    print("Testing Mooch Switch with verbose logging...")
    
    # Test OpenAI with verbose logging
    try:
        # Use verbose=True to see switching logs
        client = mooch(openai.OpenAI, verbose=True)(
            base_url=config['openai']['base_url'],
            api_keys=config['openai']['api_keys'],
        )
        response = client.chat.completions.create(
            model=config['openai']['model'],
            messages=[{"role": "user", "content": "Say hi"}],
            max_tokens=50
        )
        
        # Better handling of response content
        if response.choices and response.choices[0].message.content:
            print(f"OpenAI: {response.choices[0].message.content.strip()}")
        else:
            print(f"OpenAI: Got response but content is empty")
            print(f"Response: {response}")
            
    except Exception as e:
        print(f"OpenAI failed: {e}")
    
    print("\n" + "-" * 40 + "\n")
    
    # Test LiteLLM with verbose logging
    try:
        # Use verbose=True to see switching logs
        completion = mooch(litellm.completion, verbose=True)(
            api_keys=config['litellm']['api_keys'],
        )
        response = completion(
            model=config['litellm']['model'],
            messages=[{"role": "user", "content": "Say hi"}],
            max_tokens=50
        )
        
        # Better handling of response content
        if response.choices and response.choices[0].message.content:
            print(f"LiteLLM: {response.choices[0].message.content.strip()}")
        else:
            print(f"LiteLLM: Got response but content is empty")
            print(f"Response: {response}")
            
    except Exception as e:
        print(f"LiteLLM failed: {e}")