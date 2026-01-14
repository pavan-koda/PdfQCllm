#!/usr/bin/env python3
"""
Interactive Model Selector for PDF QA System
Comprehensive model selection including all Gemma variants and Ollama models
"""

import os
import sys
import subprocess
from typing import Dict, Optional, Tuple

class ModelSelector:
    """Interactive model selection for QA system."""

    MODELS = {
        # Ollama Vision Models
        '1': {
            'name': 'Llama 3.2-Vision (11B)',
            'type': 'ollama',
            'model_id': 'llama3.2-vision:11b',
            'description': 'Best for vision + text, handles scanned PDFs',
            'size': '7 GB',
            'vision_support': True,
            'recommended': True
        },
        '2': {
            'name': 'Llama 3.2-Vision (90B)',
            'type': 'ollama',
            'model_id': 'llama3.2-vision:90b',
            'description': 'Ultimate quality (requires 64GB+ RAM)',
            'size': '55 GB',
            'vision_support': True,
            'recommended': False
        },

        # Ollama Text Models
        '3': {
            'name': 'Llama 3.2 Text (3B)',
            'type': 'ollama',
            'model_id': 'llama3.2:3b',
            'description': 'Faster text-only model, good accuracy',
            'size': '2 GB',
            'vision_support': False,
            'recommended': False
        },
        '4': {
            'name': 'Gemma 2B',
            'type': 'ollama',
            'model_id': 'gemma:2b',
            'description': 'Google lightweight model (2B parameters)',
            'size': '1.5 GB',
            'vision_support': False,
            'recommended': False
        },
        '5': {
            'name': 'Gemma 7B',
            'type': 'ollama',
            'model_id': 'gemma:7b',
            'description': 'Google full model (7B parameters)',
            'size': '5 GB',
            'vision_support': False,
            'recommended': False
        },
        '6': {
            'name': 'Gemma 2B Instruct',
            'type': 'ollama',
            'model_id': 'gemma:2b-instruct',
            'description': 'Instruction-tuned Gemma 2B, best for QA',
            'size': '1.5 GB',
            'vision_support': False,
            'recommended': False
        },
        '7': {
            'name': 'Gemma 7B Instruct',
            'type': 'ollama',
            'model_id': 'gemma:7b-instruct',
            'description': 'Instruction-tuned Gemma 7B, premium quality',
            'size': '5 GB',
            'vision_support': False,
            'recommended': False
        },
        '8': {
            'name': 'Gemma 2 2B',
            'type': 'ollama',
            'model_id': 'gemma2:2b',
            'description': 'Gemma 2 generation, improved (2B params)',
            'size': '1.6 GB',
            'vision_support': False,
            'recommended': False
        },
        '9': {
            'name': 'Gemma 2 9B',
            'type': 'ollama',
            'model_id': 'gemma2:9b',
            'description': 'Gemma 2, state-of-the-art quality',
            'size': '5.5 GB',
            'vision_support': False,
            'recommended': True
        },
        '10': {
            'name': 'Gemma 2 27B',
            'type': 'ollama',
            'model_id': 'gemma2:27b',
            'description': 'Gemma 2 largest, exceptional quality',
            'size': '16 GB',
            'vision_support': False,
            'recommended': False
        },
        '11': {
            'name': 'Gemma 2 2B Instruct',
            'type': 'ollama',
            'model_id': 'gemma2:2b-instruct',
            'description': 'Gemma 2 instruction-tuned 2B, excellent QA',
            'size': '1.6 GB',
            'vision_support': False,
            'recommended': False
        },
        '12': {
            'name': 'Gemma 2 9B Instruct',
            'type': 'ollama',
            'model_id': 'gemma2:9b-instruct',
            'description': 'Gemma 2 instruction-tuned 9B, best quality',
            'size': '5.5 GB',
            'vision_support': False,
            'recommended': True
        },
        '13': {
            'name': 'Gemma 2 27B Instruct',
            'type': 'ollama',
            'model_id': 'gemma2:27b-instruct',
            'description': 'Gemma 2 27B instruction-tuned, top-tier',
            'size': '16 GB',
            'vision_support': False,
            'recommended': False
        },
        '14': {
            'name': 'Mistral 7B',
            'type': 'ollama',
            'model_id': 'mistral:7b',
            'description': 'Fast and accurate, general use',
            'size': '4 GB',
            'vision_support': False,
            'recommended': False
        },
        '15': {
            'name': 'Mistral 7B Instruct',
            'type': 'ollama',
            'model_id': 'mistral:7b-instruct',
            'description': 'Mistral instruction-tuned, excellent QA',
            'size': '4 GB',
            'vision_support': False,
            'recommended': False
        },
        '16': {
            'name': 'Phi-3 Mini (3.8B)',
            'type': 'ollama',
            'model_id': 'phi3:mini',
            'description': 'Microsoft compact model, fast responses',
            'size': '2.3 GB',
            'vision_support': False,
            'recommended': False
        },
        '17': {
            'name': 'Phi-3 Mini 4K Instruct',
            'type': 'ollama',
            'model_id': 'phi3:mini-4k-instruct',
            'description': 'Phi-3 instruction-tuned, strong reasoning',
            'size': '2.3 GB',
            'vision_support': False,
            'recommended': False
        },
        '18': {
            'name': 'Phi-3.5 Mini Instruct',
            'type': 'ollama',
            'model_id': 'phi3.5:mini-instruct',
            'description': 'Phi-3.5 with improved reasoning, 128K context',
            'size': '2.3 GB',
            'vision_support': False,
            'recommended': False
        },
        '19': {
            'name': 'Qwen 2.5 7B Instruct',
            'type': 'ollama',
            'model_id': 'qwen2.5:7b-instruct',
            'description': 'Alibaba Qwen, strong multilingual QA',
            'size': '4.7 GB',
            'vision_support': False,
            'recommended': False
        },
        '20': {
            'name': 'Qwen 2.5 14B Instruct',
            'type': 'ollama',
            'model_id': 'qwen2.5:14b-instruct',
            'description': 'Qwen 2.5 larger, excellent reasoning',
            'size': '9 GB',
            'vision_support': False,
            'recommended': False
        },
        '21': {
            'name': 'Custom Ollama Model',
            'type': 'ollama',
            'model_id': 'custom',
            'description': 'Enter your own Ollama model name',
            'size': 'Varies',
            'vision_support': False,
            'recommended': False
        }
    }

    def __init__(self):
        self.clear_screen()

    def clear_screen(self):
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def check_ollama_installed(self) -> bool:
        """Check if Ollama is installed."""
        try:
            result = subprocess.run(['ollama', 'list'],
                                  capture_output=True,
                                  text=True,
                                  timeout=5)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def get_installed_models(self) -> list:
        """Get list of already installed Ollama models."""
        try:
            result = subprocess.run(['ollama', 'list'],
                                  capture_output=True,
                                  text=True,
                                  timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                return [line.split()[0] for line in lines if line.strip()]
        except:
            pass
        return []

    def display_menu(self):
        """Display interactive model selection menu."""
        print("=" * 80)
        print("  PDF QA SYSTEM - COMPREHENSIVE MODEL SELECTOR")
        print("=" * 80)
        print()

        # Check Ollama status
        if not self.check_ollama_installed():
            print("WARNING: Ollama not found!")
            print("Install: https://ollama.ai/download")
            print()
        else:
            installed = self.get_installed_models()
            print(f"Ollama installed | {len(installed)} model(s) available")
            print()

        print("Available Models:")
        print("-" * 80)

        # Group models by category
        print("\n[VISION MODELS - Can read scanned PDFs, diagrams]")
        for key in ['1', '2']:
            model = self.MODELS[key]
            self._print_model(key, model)

        print("\n[GEMMA MODELS - Google, Excellent for Technical Content]")
        for key in ['4', '5', '6', '7', '8', '9', '10', '11', '12', '13']:
            model = self.MODELS[key]
            self._print_model(key, model)

        print("\n[OTHER OLLAMA MODELS]")
        for key in ['3', '14', '15', '16', '17', '18', '19', '20']:
            model = self.MODELS[key]
            self._print_model(key, model)

        print("\n[CUSTOM]")
        self._print_model('21', self.MODELS['21'])

        print("\n" + "=" * 80)
        print("\n0. Exit")
        print()

    def _print_model(self, key, model):
        """Print a single model entry."""
        installed = self.get_installed_models()
        status = "[INSTALLED]" if model['model_id'] in installed or model['model_id'] == 'custom' else "[DOWNLOAD]"
        recommended = " [RECOMMENDED]" if model.get('recommended') else ""
        vision = " [VISION]" if model.get('vision_support') else ""

        print(f"{key:>3}. {model['name']}{recommended}{vision}")
        print(f"     {model['description']}")
        print(f"     Size: {model['size']} | Status: {status}")

    def select_model(self) -> Optional[Tuple[str, str, bool]]:
        """
        Interactive model selection.

        Returns:
            Tuple of (model_type, model_id, vision_support) or None if exit
        """
        while True:
            self.display_menu()

            choice = input("Select model (1-21) or 0 to exit: ").strip()

            if choice == '0':
                print("\nExiting...")
                return None

            if choice not in self.MODELS:
                print(f"\n❌ Invalid choice: {choice}")
                input("Press Enter to continue...")
                self.clear_screen()
                continue

            model = self.MODELS[choice]

            # Handle custom model
            if model['model_id'] == 'custom':
                custom_name = input("\nEnter Ollama model name (e.g., gemma3:4b-instruct): ").strip()
                if not custom_name:
                    print("ERROR: Invalid model name")
                    input("Press Enter to continue...")
                    self.clear_screen()
                    continue

                model_id = custom_name
                has_vision = input("Does this model support vision? (y/n): ").strip().lower() == 'y'
            else:
                model_id = model['model_id']
                has_vision = model['vision_support']

            # Confirm selection
            print("\n" + "=" * 80)
            print(f"Selected: {model['name']}")
            print(f"Model ID: {model_id}")
            print(f"Vision Support: {'Yes' if has_vision else 'No'}")
            print(f"Description: {model['description']}")
            print("=" * 80)

            confirm = input("\nProceed with this model? (y/n): ").strip().lower()

            if confirm == 'y':
                # Check if model is installed
                if model_id not in self.get_installed_models():
                    print(f"\nModel not installed. Downloading {model_id}...")
                    print("This may take several minutes depending on model size.")
                    print()

                    download = input("Download now? (y/n): ").strip().lower()
                    if download == 'y':
                        try:
                            print(f"\nDownloading {model_id}...")
                            subprocess.run(['ollama', 'pull', model_id], check=True)
                            print(f"\nSUCCESS: {model_id} downloaded successfully!")
                        except subprocess.CalledProcessError:
                            print(f"\nERROR: Failed to download {model_id}")
                            input("Press Enter to continue...")
                            self.clear_screen()
                            continue
                        except KeyboardInterrupt:
                            print("\n\nERROR: Download cancelled")
                            input("Press Enter to continue...")
                            self.clear_screen()
                            continue
                    else:
                        print("ERROR: Cannot proceed without model")
                        input("Press Enter to continue...")
                        self.clear_screen()
                        continue

                return (model['type'], model_id, has_vision)

            self.clear_screen()


def select_model_interactive() -> Optional[Tuple[str, str, bool]]:
    """
    Run interactive model selector.

    Returns:
        Tuple of (model_type, model_id, vision_support) or None if exit
    """
    selector = ModelSelector()
    return selector.select_model()


if __name__ == '__main__':
    result = select_model_interactive()

    if result:
        model_type, model_id, has_vision = result
        print("\n" + "=" * 80)
        print("SELECTED CONFIGURATION")
        print("=" * 80)
        print(f"Model Type: {model_type}")
        print(f"Model ID: {model_id}")
        print(f"Vision Support: {has_vision}")
        print("=" * 80)
    else:
        print("No model selected")
