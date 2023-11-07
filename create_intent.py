from google.cloud import dialogflow
import json
import argparse

from dotenv import load_dotenv


def create_intent(project_id, display_name,
                  training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print(f"Intent created: {response}")


def main():
    parser = argparse.ArgumentParser(description='DialogFlow training script')
    parser.add_argument('--path',
                        default='questions.json',
                        help='questions file path')

    args = parser.parse_args()
    file_path = args.path

    with open(file_path, 'r', encoding='utf-8') as file:
        questions_json = file.read()

    questions = json.loads(questions_json)

    for key, value in questions.items():

        create_intent(
            project_id=config.project_id,
            display_name=key,
            training_phrases_parts=value['questions'],
            message_texts=value['answer']
        )


if __name__ == '__main__':
    load_dotenv()
    import config
    main()
