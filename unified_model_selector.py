#!/usr/bin/env python3
"""
Comprehensive Unified Model Selector for PDF QA System
Supports both Ollama and HuggingFace models
Includes all Gemma variants, GPT-2, OPT, FLAN-T5, Phi, TinyLlama, StableLM, Mistral, Qwen, Llama
"""

import os
import sys
import subprocess
from typing import Dict, Optional, Tuple
from pathlib import Path

class UnifiedModelSelector:
    """Comprehensive model selection supporting Ollama and HuggingFace."""

    MODELS = {
        # ========== OLLAMA VISION MODELS ==========
        '1': {
            'name': 'Llama 3.2-Vision (11B)',
            'type': 'ollama',
            'model_id': 'llama3.2-vision:11b',
            'description': 'Best for vision + text, handles scanned PDFs',
            'size': '7 GB',
            'speed': 'Medium',
            'vision_support': True,
            'recommended': True,
            'category': 'vision'
        },
        '2': {
            'name': 'Llama 3.2-Vision (90B)',
            'type': 'ollama',
            'model_id': 'llama3.2-vision:90b',
            'description': 'Ultimate quality (requires 64GB+ RAM)',
            'size': '55 GB',
            'speed': 'Slow',
            'vision_support': True,
            'recommended': False,
            'category': 'vision'
        },

        # ========== OLLAMA GEMMA MODELS ==========
        '3': {
            'name': 'Gemma 2B (Ollama)',
            'type': 'ollama',
            'model_id': 'gemma:2b',
            'description': 'Google lightweight model (2B parameters)',
            'size': '1.5 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_ollama'
        },
        '4': {
            'name': 'Gemma 7B (Ollama)',
            'type': 'ollama',
            'model_id': 'gemma:7b',
            'description': 'Google full model (7B parameters)',
            'size': '5 GB',
            'speed': 'Medium',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_ollama'
        },
        '5': {
            'name': 'Gemma 2B Instruct (Ollama)',
            'type': 'ollama',
            'model_id': 'gemma:2b-instruct',
            'description': 'Instruction-tuned Gemma 2B, best for QA',
            'size': '1.5 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_ollama'
        },
        '6': {
            'name': 'Gemma 7B Instruct (Ollama)',
            'type': 'ollama',
            'model_id': 'gemma:7b-instruct',
            'description': 'Instruction-tuned Gemma 7B, premium quality',
            'size': '5 GB',
            'speed': 'Medium',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_ollama'
        },
        '7': {
            'name': 'Gemma 2 2B (Ollama)',
            'type': 'ollama',
            'model_id': 'gemma2:2b',
            'description': 'Gemma 2 generation, improved (2B params)',
            'size': '1.6 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_ollama'
        },
        '8': {
            'name': 'Gemma 2 9B (Ollama)',
            'type': 'ollama',
            'model_id': 'gemma2:9b',
            'description': 'Gemma 2, state-of-the-art quality',
            'size': '5.5 GB',
            'speed': 'Medium',
            'vision_support': False,
            'recommended': True,
            'category': 'gemma_ollama'
        },
        '9': {
            'name': 'Gemma 2 27B (Ollama)',
            'type': 'ollama',
            'model_id': 'gemma2:27b',
            'description': 'Gemma 2 largest, exceptional quality',
            'size': '16 GB',
            'speed': 'Slow',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_ollama'
        },
        '10': {
            'name': 'Gemma 2 2B Instruct (Ollama)',
            'type': 'ollama',
            'model_id': 'gemma2:2b-instruct',
            'description': 'Gemma 2 instruction-tuned 2B, excellent QA',
            'size': '1.6 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_ollama'
        },
        '11': {
            'name': 'Gemma 2 9B Instruct (Ollama)',
            'type': 'ollama',
            'model_id': 'gemma2:9b-instruct',
            'description': 'Gemma 2 instruction-tuned 9B, best quality',
            'size': '5.5 GB',
            'speed': 'Medium',
            'vision_support': False,
            'recommended': True,
            'category': 'gemma_ollama'
        },
        '12': {
            'name': 'Gemma 2 27B Instruct (Ollama)',
            'type': 'ollama',
            'model_id': 'gemma2:27b-instruct',
            'description': 'Gemma 2 27B instruction-tuned, top-tier',
            'size': '16 GB',
            'speed': 'Slow',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_ollama'
        },

        # ========== HUGGINGFACE GEMMA MODELS ==========
        '13': {
            'name': 'Gemma 2B (HuggingFace)',
            'type': 'huggingface',
            'model_id': 'google/gemma-2b',
            'description': 'Google lightweight Gemma (2B params, HF)',
            'size': '5 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_hf'
        },
        '14': {
            'name': 'Gemma 7B (HuggingFace)',
            'type': 'huggingface',
            'model_id': 'google/gemma-7b',
            'description': 'Google full Gemma (7B params, requires GPU)',
            'size': '14 GB',
            'speed': 'Slow',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_hf'
        },
        '15': {
            'name': 'Gemma 2B Instruct (HuggingFace)',
            'type': 'huggingface',
            'model_id': 'google/gemma-2b-it',
            'description': 'Instruction-tuned Gemma 2B, best for QA',
            'size': '5 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_hf'
        },
        '16': {
            'name': 'Gemma 7B Instruct (HuggingFace)',
            'type': 'huggingface',
            'model_id': 'google/gemma-7b-it',
            'description': 'Instruction-tuned Gemma 7B, premium quality',
            'size': '14 GB',
            'speed': 'Slow',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_hf'
        },
        '17': {
            'name': 'Gemma 2 2B (HuggingFace)',
            'type': 'huggingface',
            'model_id': 'google/gemma-2-2b',
            'description': 'Gemma 2 generation, improved (2B params)',
            'size': '5 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_hf'
        },
        '18': {
            'name': 'Gemma 2 9B (HuggingFace)',
            'type': 'huggingface',
            'model_id': 'google/gemma-2-9b',
            'description': 'Gemma 2, state-of-the-art (requires 20GB+ VRAM)',
            'size': '18 GB',
            'speed': 'Slow',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_hf'
        },
        '19': {
            'name': 'Gemma 2 2B Instruct (HuggingFace)',
            'type': 'huggingface',
            'model_id': 'google/gemma-2-2b-it',
            'description': 'Gemma 2 instruction-tuned 2B, excellent QA',
            'size': '5 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_hf'
        },
        '20': {
            'name': 'Gemma 2 9B Instruct (HuggingFace)',
            'type': 'huggingface',
            'model_id': 'google/gemma-2-9b-it',
            'description': 'Gemma 2 instruction-tuned 9B, best quality',
            'size': '18 GB',
            'speed': 'Slow',
            'vision_support': False,
            'recommended': True,
            'category': 'gemma_hf'
        },
        '21': {
            'name': 'Gemma 2 27B Instruct (HuggingFace)',
            'type': 'huggingface',
            'model_id': 'google/gemma-2-27b-it',
            'description': 'Gemma 2 largest, top-tier quality (48GB+ VRAM)',
            'size': '54 GB',
            'speed': 'Very Slow',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_hf'
        },
        '22': {
            'name': 'Gemma 3 4B (HuggingFace)',
            'type': 'huggingface',
            'model_id': 'google/gemma-3-4b',
            'description': 'Gemma 3 compact, latest generation (4B params)',
            'size': '8 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_hf'
        },
        '23': {
            'name': 'Gemma 3 12B (HuggingFace)',
            'type': 'huggingface',
            'model_id': 'google/gemma-3-12b',
            'description': 'Gemma 3 mid-size, cutting-edge (24GB+ VRAM)',
            'size': '24 GB',
            'speed': 'Medium',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_hf'
        },
        '24': {
            'name': 'Gemma 3 4B Instruct (HuggingFace)',
            'type': 'huggingface',
            'model_id': 'google/gemma-3-4b-it',
            'description': 'Gemma 3 instruction-tuned 4B, best-in-class QA',
            'size': '8 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': True,
            'category': 'gemma_hf'
        },
        '25': {
            'name': 'Gemma 3 12B Instruct (HuggingFace)',
            'type': 'huggingface',
            'model_id': 'google/gemma-3-12b-it',
            'description': 'Gemma 3 instruction-tuned 12B, premium (24GB+ VRAM)',
            'size': '24 GB',
            'speed': 'Medium',
            'vision_support': False,
            'recommended': False,
            'category': 'gemma_hf'
        },

        # ========== OTHER OLLAMA MODELS ==========
        '26': {
            'name': 'Llama 3.2 Text (3B)',
            'type': 'ollama',
            'model_id': 'llama3.2:3b',
            'description': 'Faster text-only model, good accuracy',
            'size': '2 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'other_ollama'
        },
        '27': {
            'name': 'Mistral 7B',
            'type': 'ollama',
            'model_id': 'mistral:7b',
            'description': 'Fast and accurate, general use',
            'size': '4 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'other_ollama'
        },
        '28': {
            'name': 'Mistral 7B Instruct',
            'type': 'ollama',
            'model_id': 'mistral:7b-instruct',
            'description': 'Mistral instruction-tuned, excellent QA',
            'size': '4 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'other_ollama'
        },
        '29': {
            'name': 'Phi-3 Mini (3.8B)',
            'type': 'ollama',
            'model_id': 'phi3:mini',
            'description': 'Microsoft compact model, fast responses',
            'size': '2.3 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'other_ollama'
        },
        '30': {
            'name': 'Phi-3 Mini 4K Instruct',
            'type': 'ollama',
            'model_id': 'phi3:mini-4k-instruct',
            'description': 'Phi-3 instruction-tuned, strong reasoning',
            'size': '2.3 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'other_ollama'
        },
        '31': {
            'name': 'Phi-3.5 Mini Instruct',
            'type': 'ollama',
            'model_id': 'phi3.5:mini-instruct',
            'description': 'Phi-3.5 improved reasoning, 128K context',
            'size': '2.3 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'other_ollama'
        },
        '32': {
            'name': 'Qwen 2.5 7B Instruct',
            'type': 'ollama',
            'model_id': 'qwen2.5:7b-instruct',
            'description': 'Alibaba Qwen, strong multilingual QA',
            'size': '4.7 GB',
            'speed': 'Medium',
            'vision_support': False,
            'recommended': False,
            'category': 'other_ollama'
        },
        '33': {
            'name': 'Qwen 2.5 14B Instruct',
            'type': 'ollama',
            'model_id': 'qwen2.5:14b-instruct',
            'description': 'Qwen 2.5 larger, excellent reasoning',
            'size': '9 GB',
            'speed': 'Medium',
            'vision_support': False,
            'recommended': False,
            'category': 'other_ollama'
        },

        # ========== HUGGINGFACE GPT-2 MODELS ==========
        '34': {
            'name': 'GPT-2 Small',
            'type': 'huggingface',
            'model_id': 'gpt2',
            'description': 'Lightweight text generation (117M params)',
            'size': '500 MB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'gpt2'
        },
        '35': {
            'name': 'GPT-2 Medium',
            'type': 'huggingface',
            'model_id': 'gpt2-medium',
            'description': 'Better text generation (345M params)',
            'size': '1.5 GB',
            'speed': 'Medium',
            'vision_support': False,
            'recommended': False,
            'category': 'gpt2'
        },
        '36': {
            'name': 'GPT-2 Large',
            'type': 'huggingface',
            'model_id': 'gpt2-large',
            'description': 'High-quality text generation (774M params)',
            'size': '3 GB',
            'speed': 'Slower',
            'vision_support': False,
            'recommended': False,
            'category': 'gpt2'
        },
        '37': {
            'name': 'GPT-2 XL',
            'type': 'huggingface',
            'model_id': 'gpt2-xl',
            'description': 'Best GPT-2 model (1.5B params, requires GPU)',
            'size': '6 GB',
            'speed': 'Very Slow',
            'vision_support': False,
            'recommended': False,
            'category': 'gpt2'
        },

        # ========== HUGGINGFACE OTHER MODELS ==========
        '38': {
            'name': 'OPT-350M',
            'type': 'huggingface',
            'model_id': 'facebook/opt-350m',
            'description': "Meta's OPT - efficient GPT-2 alternative",
            'size': '700 MB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },
        '39': {
            'name': 'OPT-1.3B',
            'type': 'huggingface',
            'model_id': 'facebook/opt-1.3b',
            'description': 'Larger OPT for better generation',
            'size': '2.5 GB',
            'speed': 'Medium',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },
        '40': {
            'name': 'FLAN-T5 Small',
            'type': 'huggingface',
            'model_id': 'google/flan-t5-small',
            'description': "Google's instruction-tuned, good for QA",
            'size': '300 MB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },
        '41': {
            'name': 'FLAN-T5 Base',
            'type': 'huggingface',
            'model_id': 'google/flan-t5-base',
            'description': 'Better FLAN-T5, excellent for answering',
            'size': '900 MB',
            'speed': 'Medium',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },
        '42': {
            'name': 'FLAN-T5 Large',
            'type': 'huggingface',
            'model_id': 'google/flan-t5-large',
            'description': 'Large instruction-tuned, best for QA',
            'size': '3 GB',
            'speed': 'Slower',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },
        '43': {
            'name': 'Phi-2',
            'type': 'huggingface',
            'model_id': 'microsoft/phi-2',
            'description': "Microsoft's 2.7B, high quality reasoning",
            'size': '5.5 GB',
            'speed': 'Medium',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },
        '44': {
            'name': 'TinyLlama Chat',
            'type': 'huggingface',
            'model_id': 'TinyLlama/TinyLlama-1.1B-Chat-v1.0',
            'description': 'Compact Llama-based chat (1.1B params)',
            'size': '2.2 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },
        '45': {
            'name': 'StableLM Zephyr 1.6B',
            'type': 'huggingface',
            'model_id': 'stabilityai/stablelm-2-zephyr-1_6b',
            'description': 'Stability AI instruction-tuned model',
            'size': '3 GB',
            'speed': 'Medium',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },
        '46': {
            'name': 'Llama 2 7B Chat',
            'type': 'huggingface',
            'model_id': 'meta-llama/Llama-2-7b-chat-hf',
            'description': "Meta's Llama 2 chat (requires HF auth, 16GB VRAM)",
            'size': '13 GB',
            'speed': 'Slow',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },
        '47': {
            'name': 'Llama 2 13B Chat',
            'type': 'huggingface',
            'model_id': 'meta-llama/Llama-2-13b-chat-hf',
            'description': 'Larger Llama 2 (requires HF auth, 24GB+ VRAM)',
            'size': '26 GB',
            'speed': 'Very Slow',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },
        '48': {
            'name': 'Mistral 7B Instruct (HF)',
            'type': 'huggingface',
            'model_id': 'mistralai/Mistral-7B-Instruct-v0.3',
            'description': 'Mistral AI instruction-tuned, excellent QA',
            'size': '14 GB',
            'speed': 'Medium',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },
        '49': {
            'name': 'Mistral 12B Instruct (HF)',
            'type': 'huggingface',
            'model_id': 'mistralai/Mistral-12B-Instruct-v0.3',
            'description': 'Mistral AI larger, top-tier reasoning (12B)',
            'size': '24 GB',
            'speed': 'Slower',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },
        '50': {
            'name': 'Phi-3 Mini 4K (HF)',
            'type': 'huggingface',
            'model_id': 'microsoft/Phi-3-mini-4k-instruct',
            'description': 'Microsoft compact, strong reasoning (3.8B, 4K)',
            'size': '7.5 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },
        '51': {
            'name': 'Phi-3.5 Mini (HF)',
            'type': 'huggingface',
            'model_id': 'microsoft/Phi-3.5-mini-instruct',
            'description': 'Phi-3.5 improved reasoning (3.8B, 128K)',
            'size': '7.5 GB',
            'speed': 'Fast',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },
        '52': {
            'name': 'Qwen 2.5 7B Instruct (HF)',
            'type': 'huggingface',
            'model_id': 'Qwen/Qwen2.5-7B-Instruct',
            'description': 'Alibaba Qwen, strong multilingual QA (7B)',
            'size': '14 GB',
            'speed': 'Medium',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },
        '53': {
            'name': 'Qwen 2.5 14B Instruct (HF)',
            'type': 'huggingface',
            'model_id': 'Qwen/Qwen2.5-14B-Instruct',
            'description': 'Qwen 2.5 larger, excellent reasoning (14B)',
            'size': '28 GB',
            'speed': 'Slower',
            'vision_support': False,
            'recommended': False,
            'category': 'other_hf'
        },

        # ========== CUSTOM ==========
        '99': {
            'name': 'Custom Model',
            'type': 'custom',
            'model_id': 'custom',
            'description': 'Enter your own Ollama or HuggingFace model',
            'size': 'Varies',
            'speed': 'Varies',
            'vision_support': False,
            'recommended': False,
            'category': 'custom'
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
        """Display comprehensive model selection menu."""
        print("=" * 80)
        print("  PDF QA SYSTEM - COMPREHENSIVE MODEL SELECTOR")
        print("=" * 80)
        print()

        # Check Ollama status
        ollama_installed = self.check_ollama_installed()
        if not ollama_installed:
            print("WARNING: Ollama not found!")
            print("Install: https://ollama.ai/download")
            print("(Required for Ollama models only)")
            print()
        else:
            installed = self.get_installed_models()
            print(f"Ollama installed | {len(installed)} model(s) available")
            print()

        print("Available Models:")
        print("-" * 80)

        # Group models by category
        categories = {
            'vision': '[VISION MODELS - Can read scanned PDFs, diagrams]',
            'gemma_ollama': '[GEMMA MODELS - Ollama (Fast setup, easy use)]',
            'gemma_hf': '[GEMMA MODELS - HuggingFace (More variants, GPU optimized)]',
            'other_ollama': '[OTHER OLLAMA MODELS - Llama, Mistral, Phi, Qwen]',
            'gpt2': '[GPT-2 MODELS - HuggingFace (Text generation)]',
            'other_hf': '[OTHER HUGGINGFACE MODELS - OPT, FLAN-T5, TinyLlama, etc.]',
            'custom': '[CUSTOM]'
        }

        for category, header in categories.items():
            models_in_category = [(k, v) for k, v in self.MODELS.items()
                                 if v.get('category') == category]
            if models_in_category:
                print(f"\n{header}")
                for key, model in models_in_category:
                    self._print_model(key, model, ollama_installed)

        print("\n" + "=" * 80)
        print("\n0. Exit")
        print()

    def _print_model(self, key, model, ollama_installed):
        """Print a single model entry."""
        # Determine installation status
        if model['type'] == 'ollama':
            if not ollama_installed:
                status = "[NEEDS OLLAMA]"
            else:
                installed = self.get_installed_models()
                status = "[INSTALLED]" if model['model_id'] in installed else "[DOWNLOAD]"
        elif model['type'] == 'huggingface':
            # Check if model is cached
            cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
            model_cache = cache_dir / f"models--{model['model_id'].replace('/', '--')}"
            status = "[CACHED]" if model_cache.exists() else "[DOWNLOAD]"
        else:  # custom
            status = "[CUSTOM]"

        recommended = " [RECOMMENDED]" if model.get('recommended') else ""
        vision = " [VISION]" if model.get('vision_support') else ""

        print(f"{key:>3}. {model['name']}{recommended}{vision}")
        print(f"     {model['description']}")
        print(f"     Size: {model['size']} | Speed: {model['speed']} | Status: {status}")

    def select_model(self) -> Optional[Tuple[str, str, bool]]:
        """
        Interactive model selection.

        Returns:
            Tuple of (model_type, model_id, vision_support) or None if exit
        """
        while True:
            self.display_menu()

            choice = input("Select model (1-53, 99 for custom) or 0 to exit: ").strip()

            if choice == '0':
                print("\nExiting...")
                return None

            if choice not in self.MODELS:
                print(f"\nERROR: Invalid choice: {choice}")
                input("Press Enter to continue...")
                self.clear_screen()
                continue

            model = self.MODELS[choice]

            # Handle custom model
            if model['model_id'] == 'custom':
                print("\nCustom Model Setup")
                print("1. Ollama model (e.g., llama3.1:8b)")
                print("2. HuggingFace model (e.g., EleutherAI/gpt-neo-1.3B)")
                model_type_choice = input("Select type (1 or 2): ").strip()

                if model_type_choice == '1':
                    model_type = 'ollama'
                    custom_name = input("\nEnter Ollama model name: ").strip()
                elif model_type_choice == '2':
                    model_type = 'huggingface'
                    custom_name = input("\nEnter HuggingFace model ID: ").strip()
                else:
                    print("ERROR: Invalid model type")
                    input("Press Enter to continue...")
                    self.clear_screen()
                    continue

                if not custom_name:
                    print("ERROR: Invalid model name")
                    input("Press Enter to continue...")
                    self.clear_screen()
                    continue

                model_id = custom_name
                has_vision = input("Does this model support vision? (y/n): ").strip().lower() == 'y'
            else:
                model_type = model['type']
                model_id = model['model_id']
                has_vision = model['vision_support']

            # Confirm selection
            print("\n" + "=" * 80)
            print(f"Selected: {model['name']}")
            print(f"Model ID: {model_id}")
            print(f"Type: {model_type}")
            print(f"Vision Support: {'Yes' if has_vision else 'No'}")
            print(f"Description: {model['description']}")
            print("=" * 80)

            confirm = input("\nProceed with this model? (y/n): ").strip().lower()

            if confirm == 'y':
                # Handle Ollama model download
                if model_type == 'ollama':
                    if not self.check_ollama_installed():
                        print("\nERROR: Ollama not installed!")
                        print("Install from: https://ollama.ai/download")
                        input("Press Enter to continue...")
                        self.clear_screen()
                        continue

                    if model_id not in self.get_installed_models():
                        print(f"\nModel not installed. Downloading {model_id}...")
                        print("This may take several minutes.")
                        print()

                        download = input("Download now? (y/n): ").strip().lower()
                        if download == 'y':
                            try:
                                print(f"\nDownloading {model_id}...")
                                subprocess.run(['ollama', 'pull', model_id], check=True)
                                print(f"\nSUCCESS: {model_id} downloaded!")
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

                # HuggingFace models will be downloaded on first use
                elif model_type == 'huggingface':
                    print("\nNOTE: HuggingFace model will be downloaded on first use")
                    print("Make sure you have sufficient disk space and GPU memory")

                return (model_type, model_id, has_vision)

            self.clear_screen()


def select_model_interactive() -> Optional[Tuple[str, str, bool]]:
    """
    Run interactive model selector.

    Returns:
        Tuple of (model_type, model_id, vision_support) or None if exit
    """
    selector = UnifiedModelSelector()
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
