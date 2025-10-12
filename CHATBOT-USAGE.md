# 💬 AI Chatbot Usage Guide

## Overview

The AI Chatbot feature provides **instant, conversational AI insights** about your LGBTQ+ Sexual Fluidity survey results. Unlike the Advanced Analysis which requires 30+ survey submissions for statistical validity, the chatbot works with just **a single submission**.

## What's the Difference?

### 🔬 Advanced Analysis (Get AI Insights Button)
- **Requirements**: Minimum 30 survey submissions
- **Method**: Two-Way ANOVA statistical analysis
- **Purpose**: Population-level insights with statistical significance
- **Output**: Statistical tables, p-values, effect sizes, interaction plots
- **Use Case**: Research, identifying patterns across large datasets

### 💬 AI Chatbot
- **Requirements**: Just 1 survey submission
- **Method**: AI-powered conversational analysis
- **Purpose**: Personalized, immediate insights about YOUR results
- **Output**: Natural language responses, contextual suggestions
- **Use Case**: Personal understanding, self-reflection, guidance

## How to Use the Chatbot

### Step 1: Complete the Survey
Fill out all 12 questions in the LGBTQ+ Sexual Fluidity survey and submit.

### Step 2: View Your Results
After submission, you'll see:
- Your overall fluidity score
- Section breakdown (Media, Family, Community, etc.)
- Interpretation with emoji and description

### Step 3: Open the Chatbot
Scroll down below your results to find the **💬 Chat with AI Assistant** section with a beautiful purple gradient interface.

### Step 4: Start Conversing
The chatbot will greet you with a welcome message. You can:

1. **Click Suggested Questions** - Quick buttons with pre-generated questions based on your scores
2. **Type Your Own Questions** - Ask anything about your results in the chat input

## Sample Questions to Ask

### Understanding Your Scores
- "What do my scores mean?"
- "Can you explain my results in simple terms?"
- "Why is my overall score [X]?"
- "What does my [section name] score indicate?"

### Personal Insights (Thai)
- "คะแนนของฉันหมายความว่าอย่างไร?"
- "ฉันควรทำอย่างไรต่อไป?"
- "มีคำแนะนำอะไรสำหรับฉันไหม?"

### Reflective Questions
- "How can I better understand my sexual fluidity?"
- "What factors might be influencing my experiences?"
- "Are my experiences common?"
- "Should I be concerned about anything?"

### Next Steps
- "What should I do next?"
- "How can I explore this further?"
- "Are there resources you recommend?"
- "Who can I talk to about this?"

## Features

### 🎯 Context-Aware Responses
The chatbot has full access to your survey results, including:
- All 12 individual question scores
- Section scores (Media, Family, Community, Culture, Exploration, School)
- Overall fluidity score
- Your language preference (Thai/English)

### 💡 Dynamic Suggestions
After each response, the chatbot generates **4 relevant follow-up questions** based on:
- Your previous question
- Your scores in different sections
- Common concerns related to your results

### 🌐 Bilingual Support
- **Thai (ไทย)**: Full support with culturally appropriate responses
- **English**: Natural, supportive language

### 🔒 Privacy-Focused
- No conversation history stored permanently
- Only last 5 messages kept in memory for context
- All data processed in real-time

## Example Conversation

**User:** What do my scores mean?

**AI Assistant:** 🌈 Based on your survey results, your overall sexual fluidity score is 65.5%, which indicates a **moderate level** of sexual fluidity.

Looking at your section scores:
- **Media Influence**: 75% - You're quite influenced by media representation
- **Family**: 50% - Moderate family influence
- **Community**: 60% - Good community support
- **Culture**: 70% - Cultural factors play a significant role
- **Exploration**: 80% - High openness to exploration
- **School**: 55% - Moderate school environment impact

Your high exploration score (80%) combined with moderate family influence (50%) suggests you're actively navigating your identity while balancing family expectations.

**Suggested Questions:**
- "What does my high media influence mean?"
- "How can I talk to my family about this?"
- "Is 65% considered high or low?"
- "What resources can help me explore further?"

---

**User:** How can I talk to my family about this?

**AI Assistant:** 💜 Talking to family can be challenging, especially with your moderate family influence score (50%). Here are some supportive suggestions:

1. **Assess Readiness**: Only share when YOU feel ready and safe
2. **Start Small**: Test the waters with trusted family members first
3. **Educate**: Share resources about sexual fluidity
4. **Set Boundaries**: You don't owe anyone your personal journey details
5. **Seek Support**: Consider LGBTQ+ support groups or counselors

Your cultural score (70%) suggests cultural context matters in your family. Consider culturally sensitive approaches or find LGBTQ+ organizations familiar with your cultural background.

**Suggested Questions:**
- "Are there Thai LGBTQ+ support organizations?"
- "What if my family reacts negatively?"
- "How do I know if it's safe to come out?"
- "Can you recommend counseling services?"

## Technical Details

### Endpoint
- **URL**: `POST /api/chatbot`
- **Rate Limit**: 20 requests per minute
- **Timeout**: 10 seconds

### Request Format
```json
{
  "survey_result": {
    "media1": 4,
    "media2": 5,
    "family1": 3,
    "family2": 2,
    "family3": 3,
    "community1": 4,
    "community2": 3,
    "culture1": 4,
    "culture2": 4,
    "exploration1": 5,
    "exploration2": 5,
    "school1": 3
  },
  "message": "What do my scores mean?",
  "conversation_history": [
    { "role": "assistant", "content": "Hello! How can I help?" },
    { "role": "user", "content": "Hi there" }
  ],
  "language": "en"
}
```

### Response Format
```json
{
  "message": "Based on your scores...",
  "suggestions": [
    "What does my high media influence mean?",
    "How can I talk to my family?",
    "What resources are available?",
    "Should I seek counseling?"
  ]
}
```

## AI Models Used

### Google Gemini 2.5 Flash (Primary)
- **Cost**: Free forever (as of 2024)
- **Speed**: Fast responses (1-2 seconds)
- **Quality**: High-quality, contextual responses
- **Language**: Excellent bilingual support (Thai/English)

### OpenAI (Fallback)
- **Model**: GPT-4o-mini
- **Cost**: Pay-per-use (backup only)
- **Activation**: Only if Gemini fails

## Limitations

### What the Chatbot CAN Do
✅ Explain your individual results  
✅ Provide personalized insights  
✅ Suggest resources and next steps  
✅ Answer questions about sexual fluidity  
✅ Offer emotional support and validation  
✅ Guide you through self-reflection  

### What the Chatbot CANNOT Do
❌ Provide medical or psychiatric diagnoses  
❌ Replace professional therapy/counseling  
❌ Perform statistical analysis across populations  
❌ Guarantee specific outcomes or predictions  
❌ Store your data permanently  
❌ Contact emergency services (if in crisis, please call your local hotline)  

## Troubleshooting

### Chatbot Not Responding
1. **Check Internet**: Ensure stable connection
2. **Wait a Moment**: AI processing can take 1-3 seconds
3. **Refresh Page**: Reload if stuck
4. **Check Errors**: Look for red error messages

### Getting Generic Responses
- **Be Specific**: Ask about particular scores or sections
- **Provide Context**: Mention what concerns you
- **Follow Suggestions**: Use the suggested questions as templates

### Rate Limit Error
- **Wait 1 Minute**: You've sent 20+ messages in one minute
- **Slow Down**: Take time to read AI responses fully

## Privacy & Ethics

### Data Handling
- Survey results sent with each message for context
- Conversation history limited to last 5 messages
- No permanent storage of conversations
- No third-party sharing

### AI Limitations
The chatbot is powered by AI and may:
- Make mistakes or provide inaccurate information
- Reflect biases present in training data
- Not fully understand cultural nuances
- Give general advice that may not apply to you

**Always prioritize your safety and wellbeing. If you're in crisis, contact a professional helpline immediately.**

## Support Resources

### LGBTQ+ Hotlines
- **Thailand**: [Insert local Thai LGBTQ+ hotline]
- **International**: The Trevor Project (for youth): 1-866-488-7386

### Online Resources
- [Local LGBTQ+ organizations]
- [Supportive communities]
- [Educational resources]

## Feedback

Found a bug or have suggestions? Please open an issue on GitHub or contact the development team.

---

**Remember**: Sexual fluidity is a personal journey. The chatbot is here to support your self-discovery, not define your identity. You are the expert on your own experiences. 🌈💜
