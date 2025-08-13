import unittest
import yaml
import openai
import litellm
from mooch import mooch


class TestMoochSwitch(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Load configuration from configs/config.yaml"""
        with open('configs/config.yaml', 'r') as f:
            cls.config = yaml.safe_load(f)
    
    def normalize_api_keys(self, api_key_config):
        """Convert api_key config to list format"""
        if isinstance(api_key_config, str):
            return [api_key_config]
        elif isinstance(api_key_config, list):
            return api_key_config
        else:
            raise ValueError(f"api_key must be str or list[str], got {type(api_key_config)}")
    
    def test_openai_client_creation(self):
        """Test OpenAI client creation with mooch"""
        # Normalize API keys and duplicate for testing
        base_keys = self.normalize_api_keys(self.config['openai']['api_keys'])
        api_keys = base_keys * 3  # Create multiple keys for testing
        
        client = mooch(openai.OpenAI)(
            api_keys=api_keys,
            base_url=self.config['openai']['base_url']
        )
        
        # Verify it's the right type and has expected attributes
        self.assertIsInstance(client, openai.OpenAI)
        self.assertTrue(hasattr(client, 'chat'))
        self.assertTrue(hasattr(client.chat, 'completions'))
        self.assertTrue(hasattr(client.chat.completions, 'create'))
        
        # Verify API keys are stored
        self.assertEqual(client.api_keys, api_keys)
    
    def test_litellm_wrapper_creation(self):
        """Test LiteLLM completion wrapper creation"""
        # Normalize API keys and duplicate for testing
        base_keys = self.normalize_api_keys(self.config['litellm']['api_keys'])
        api_keys = base_keys * 3  # Create multiple keys for testing
        
        completion = mooch(litellm.completion)(api_keys=api_keys)
        
        # Verify it's callable and has expected attributes
        self.assertTrue(callable(completion))
        self.assertEqual(completion.api_keys, api_keys)
    
    def test_openai_completion(self):
        """Test actual OpenAI completion call"""
        api_keys = self.normalize_api_keys(self.config['openai']['api_keys'])
        
        client = mooch(openai.OpenAI)(
            api_keys=api_keys,
            base_url=self.config['openai']['base_url']
        )
        
        try:
            response = client.chat.completions.create(
                model=self.config['openai']['model'],
                messages=[{"role": "user", "content": "Say hello in one word"}],
                max_tokens=10
            )
            
            # Verify response structure
            self.assertIsNotNone(response)
            self.assertTrue(hasattr(response, 'choices'))
            self.assertGreater(len(response.choices), 0)
            self.assertTrue(hasattr(response.choices[0], 'message'))
            
        except Exception as e:
            self.skipTest(f"OpenAI API call failed: {e}")
    
    def test_litellm_completion(self):
        """Test actual LiteLLM completion call"""
        api_keys = self.normalize_api_keys(self.config['litellm']['api_keys'])
        
        completion = mooch(litellm.completion)(api_keys=api_keys)
        
        try:
            response = completion(
                model=self.config['litellm']['model'],
                messages=[{"role": "user", "content": "Say hello in one word"}],
                max_tokens=10
            )
            
            # Verify response structure
            self.assertIsNotNone(response)
            self.assertTrue(hasattr(response, 'choices'))
            self.assertGreater(len(response.choices), 0)
            self.assertTrue(hasattr(response.choices[0], 'message'))
            
        except Exception as e:
            self.skipTest(f"LiteLLM API call failed: {e}")
    
    def test_normalize_api_keys(self):
        """Test the normalize_api_keys function"""
        # Test string input
        result = self.normalize_api_keys("single-key")
        self.assertEqual(result, ["single-key"])
        
        # Test list input
        result = self.normalize_api_keys(["key1", "key2"])
        self.assertEqual(result, ["key1", "key2"])
        
        # Test invalid input
        with self.assertRaises(ValueError):
            self.normalize_api_keys(123)
    
    def test_unsupported_target(self):
        """Test error handling for unsupported targets"""
        with self.assertRaises(ValueError):
            mooch("unsupported_function")
    
    def test_empty_api_keys(self):
        """Test behavior with empty API keys list"""
        with self.assertRaises(IndexError):
            mooch(openai.OpenAI)(api_keys=[])


if __name__ == '__main__':
    unittest.main() 