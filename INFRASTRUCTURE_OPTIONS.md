# Infrastructure & Hosting Options

## Current Setup
- **Hosting**: Railway (paid tier, limited free hours)
- **Database**: In-memory (resets on redeploy)
- **LLM**: OpenAI GPT-4o via API

## Long-term Cost-Effective Options

### 1. Azure AI (Professor Access Available) ✅
**Status**: Resource created, credentials ready

**Benefits**:
- Academic pricing/free credits
- Azure OpenAI Service (GPT-4, GPT-3.5)
- Phi-3/Phi-4 models (small, fast, FREE)
- Could host backend on Azure App Service

**Next Steps**:
- Set up Azure OpenAI endpoint
- Test Phi-4 for field note generation (smaller/cheaper)
- Explore Azure free tier for hosting

### 2. AWS (Professor Access Available) ✅
**Status**: AWS Trainium access mentioned in email

**Notes**:
- **AWS Trainium**: For training models, NOT inference - probably not relevant
- **AWS EC2 Spot Instances**: Could run backend much cheaper than Railway
- **AWS Bedrock**: Claude, Llama models via API
- **AWS Lambda + DynamoDB**: Serverless option, pay only when running

**Next Steps**:
- Check if academic AWS credits available
- Consider EC2 spot instances for long-running simulations
- AWS Bedrock for model diversity

### 3. Google AI Studio / Vertex AI
**Benefits**:
- **Gemini 2.5 Flash**: Very fast, generous free tier
- **Gemini 2.0 Flash Thinking**: Best reasoning model, cheap
- Google Cloud academic credits often available

**Next Steps**:
- Sign up for Google AI Studio (free tier)
- Test Gemini 2.5 Flash for descriptions
- Compare quality vs GPT-4o

### 4. Modern Fast/Cheap Models to Support

**Gemini 2.5 Flash** (Google)
- Extremely fast
- Very cheap ($0.0001875/1K tokens)
- Generous free tier
- Good at creative writing

**Qwen 2.5** (Alibaba)
- Can run locally or via Together.ai
- Extremely fast
- Good quality for size
- Free via Ollama (local)

**DeepSeek V3** (DeepSeek)
- GPT-4 level quality
- Extremely cheap ($0.27/M input tokens)
- Good at creative tasks

**Phi-4** (Microsoft)
- Small but powerful
- Free via Azure AI
- Fast inference

### 5. Alternative Hosting Platforms

**Vercel + Convex** (Like AI Town uses)
- Better free tier than Railway
- Real-time database included
- Vector search built-in
- Auto-scaling

**Render**
- Similar to Railway
- Slightly better free tier
- PostgreSQL included

**Fly.io**
- Better pricing than Railway
- Can run persistently
- PostgreSQL included

## Recommendations

### Short-term (Next 2 weeks)
1. Add Gemini 2.5 Flash support (free tier testing)
2. Set up Azure OpenAI with academic credentials
3. Test Phi-4 for cost comparison

### Medium-term (1-2 months)
1. Migrate from Railway to Azure App Service or AWS EC2
2. Implement database persistence (PostgreSQL or Convex)
3. Support multiple LLM backends (Gemini, Azure, OpenAI)

### Long-term (3-6 months)
1. Local Ollama support for offline/free operation
2. Vector embeddings for semantic memory (like AI Town)
3. Hybrid approach: cheap models for routine, GPT-4 for key moments

## Cost Comparison (per 1M tokens)

| Provider | Model | Input Cost | Output Cost |
|----------|-------|------------|-------------|
| OpenAI | GPT-4o | $2.50 | $10.00 |
| Google | Gemini 2.5 Flash | $0.1875 | $0.75 |
| DeepSeek | DeepSeek V3 | $0.27 | $1.10 |
| Azure | Phi-4 | FREE | FREE |
| Anthropic | Claude 3.5 Sonnet | $3.00 | $15.00 |

**For our use case** (generating ~300 tokens per interaction):
- 100 interactions with GPT-4o: ~$0.30
- 100 interactions with Gemini 2.5 Flash: ~$0.02
- 100 interactions with Phi-4 (Azure): FREE

## Action Items
- [ ] Test Azure OpenAI with professor credentials
- [ ] Implement Gemini 2.5 Flash support
- [ ] Compare quality: GPT-4o vs Gemini vs Phi-4
- [ ] Research Vercel + Convex migration
- [ ] Set up cost monitoring/budgets
