from text_ai.services.rag.embedding_service import get_embedding
from text_ai.services.rag.vector_store import VectorStore
from text_ai.utils.logger import get_logger

logger = get_logger()

store = VectorStore()

# memory reconstruction knowledge base

memory_dataset = [
    # family memories
    "Family gatherings commonly involve parents, children, grandparents, cousins, shared meals, celebrations, conversations, and photographs.",
    "Many memorable family moments occur during birthdays, weddings, graduations, holidays, reunions, and vacations.",
    "Children are frequently photographed while smiling, playing, interacting with family members, or celebrating special occasions.",
    "Parents often remember moments involving their children through photographs, sounds, locations, and emotional experiences.",
    # childhood memories
    "Childhood memories often involve school events, playgrounds, sports activities, teachers, classmates, family outings, and neighborhood friendships.",
    "Many childhood memories contain sensory details such as food smells, weather conditions, sounds, and familiar locations.",
    "Outdoor childhood memories frequently include parks, gardens, playgrounds, sports grounds, and community gatherings.",
    # photographic memories
    "Photographs frequently preserve memories of family events, vacations, birthdays, graduations, festivals, and social gatherings.",
    "A smiling person in a photograph often indicates a positive emotional atmosphere, although the exact emotion should not be assumed.",
    "Family photographs frequently capture interactions, shared experiences, celebrations, and meaningful life events.",
    "Photographs provide visual clues that may help reconstruct locations, activities, relationships, and events.",
    # audio interpretation
    "Public announcements are commonly heard at parks, festivals, sporting events, transportation hubs, schools, fairs, and community gatherings.",
    "Crowd noise often suggests public events, celebrations, ceremonies, markets, festivals, or social gatherings.",
    "Music frequently appears in memories involving weddings, celebrations, festivals, religious events, and family gatherings.",
    "Environmental sounds can provide clues about location, event type, atmosphere, and nearby activities.",
    # food and memory
    "Food aromas are powerful memory triggers and are often associated with family traditions, celebrations, holidays, and social gatherings.",
    "Street food vendors commonly appear at festivals, fairs, parks, public events, and community celebrations.",
    "The smell of food may help identify locations, events, cultural activities, and social experiences.",
    # parks and memory
    "Parks frequently host family outings, picnics, recreational activities, children's play, community events, and celebrations.",
    "Families often gather in parks during pleasant weather for relaxation, social interaction, and outdoor activities.",
    "Parks may contain food vendors, public announcements, entertainment activities, and community events.",
    # festivals
    "Community festivals commonly include music, food vendors, public announcements, games, performances, and large groups of people.",
    "Festivals often generate memorable experiences through sensory cues such as sounds, smells, visual decorations, and social interactions.",
    "Family attendance is common at local festivals and community celebrations.",
    # social events and memory
    "Social gatherings often involve conversations, shared meals, photographs, laughter, announcements, music, and group activities.",
    "Celebrations frequently combine multiple sensory experiences including food, sound, visual decorations, and emotional significance.",
    # weather and memory
    "Pleasant weather often encourages outdoor activities, family gatherings, photography, festivals, and recreational events.",
    "Sunny weather commonly appears in memories involving parks, vacations, community events, and family outings.",
    # memory reconstruction
    "Memory reconstruction combines partial clues from multiple sources to estimate the most likely scene or event.",
    "Visual clues, audio clues, location clues, people, activities, and sensory information can be combined to rebuild forgotten experiences.",
    "Strong memory reconstruction relies on integrating multiple independent clues rather than relying on a single detail.",
    "When exact details are unavailable, memory reconstruction should generate the most plausible scene supported by evidence.",
    "Memory reconstruction should prioritize coherence, context, and available evidence while avoiding fabrication.",
    # emotional significance
    "Positive memories often involve family connection, social interaction, celebrations, recreation, achievement, and shared experiences.",
    "Emotionally meaningful memories are often reinforced by photographs, familiar voices, sensory experiences, and important relationships.",
    # multimodal reconstruction
    "Combining image observations, audio observations, and textual descriptions often provides a more complete reconstruction than any single source alone.",
    "Multimodal memory reconstruction uses visual, auditory, and contextual evidence to infer likely events and situations.",
    "Multiple weak clues may collectively reveal a strong and coherent memory reconstruction.",
]


def initialize_vector_database():
    logger.info("Initializing Memory Reconstruction Knowledge Base...")
    count = 0
    for memory in memory_dataset:
        embedding = get_embedding(memory)
        store.add(embedding, memory)
        count += 1
        logger.info(f"Embedded knowledge item {count}")
    store.save()
    logger.info(f"Knowledge base initialized successfully with {count} entries.")


if __name__ == "__main__":
    initialize_vector_database()
