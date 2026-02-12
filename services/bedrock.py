"""AWS Bedrock service for embeddings and inference using Amazon models."""

import json
from typing import List, Optional
import boto3
from botocore.config import Config


class BedrockService:
    """Service for AWS Bedrock operations using Amazon Nova and Titan models."""

    def __init__(
        self,
        region: str,
        embedding_model: str,
        inference_model: str,
        access_key_id: Optional[str] = None,
        secret_access_key: Optional[str] = None,
    ):
        """
        Initialize Bedrock service.

        Args:
            region: AWS region
            embedding_model: Model ID for embeddings (e.g., amazon.titan-embed-text-v2:0)
            inference_model: Model ID for inference (e.g., amazon.nova-pro-v1:0)
            access_key_id: AWS access key ID (optional, uses default credentials if not provided)
            secret_access_key: AWS secret access key (optional)
        """
        config = Config(region_name=region)

        if access_key_id and secret_access_key:
            self.client = boto3.client(
                "bedrock-runtime",
                config=config,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
            )
        else:
            self.client = boto3.client("bedrock-runtime", config=config)

        self.embedding_model = embedding_model
        self.inference_model = inference_model

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using Amazon Titan Embed model.

        Args:
            text: Input text to embed

        Returns:
            List of embedding values
        """
        try:
            payload = {"inputText": text}

            response = self.client.invoke_model(
                modelId=self.embedding_model,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload),
            )

            response_body = json.loads(response["body"].read())
            return response_body["embedding"]

        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of input texts

        Returns:
            List of embeddings
        """
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings

    def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate text completion using Amazon Nova model.

        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated text
        """
        try:
            # Amazon Nova uses messages format
            messages = []

            if system_prompt:
                messages.append({
                    "role": "user",
                    "content": [{"text": f"System: {system_prompt}\n\nUser: {prompt}"}]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": [{"text": prompt}]
                })

            payload = {
                "messages": messages,
                "inferenceConfig": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                }
            }

            response = self.client.converse(
                modelId=self.inference_model,
                messages=payload["messages"],
                inferenceConfig=payload["inferenceConfig"],
            )

            # Extract text from response
            output_message = response["output"]["message"]
            text_content = output_message["content"][0]["text"]

            return text_content

        except Exception as e:
            print(f"Error generating completion: {e}")
            raise

    def chat(
        self,
        messages: List[dict],
        system_prompt: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate chat completion using Amazon Nova model.

        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: System prompt (optional)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated text
        """
        try:
            # Convert messages to Nova format
            nova_messages = []

            # Add system prompt to first user message if provided
            if system_prompt and messages:
                first_msg = messages[0]
                if first_msg["role"] == "user":
                    nova_messages.append({
                        "role": "user",
                        "content": [{"text": f"System: {system_prompt}\n\nUser: {first_msg['content']}"}]
                    })
                    messages = messages[1:]
                else:
                    nova_messages.append({
                        "role": "user",
                        "content": [{"text": f"System: {system_prompt}"}]
                    })

            # Convert remaining messages
            for msg in messages:
                nova_messages.append({
                    "role": msg["role"],
                    "content": [{"text": msg["content"]}]
                })

            response = self.client.converse(
                modelId=self.inference_model,
                messages=nova_messages,
                inferenceConfig={
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                }
            )

            output_message = response["output"]["message"]
            text_content = output_message["content"][0]["text"]

            return text_content

        except Exception as e:
            print(f"Error in chat: {e}")
            raise
