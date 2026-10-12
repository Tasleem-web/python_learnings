# Complete Guide: AI SDLC in Angular

## Table of Contents
1. [Introduction](#introduction)
2. [Architecture Diagram](#architecture)
3. [Phase-by-Phase Breakdown](#phases)
4. [Step-by-Step Examples](#examples)
5. [Resources](#resources)
6. [Complete Working Example](#complete-example)
7. [Extra Features & Best Practices](#extra-features)

---

## 1. Introduction to AI SDLC

### What is AI SDLC?
AI Software Development Life Cycle (AI SDLC) integrates artificial intelligence at every development stage. In Angular, this means building AI-powered apps and using AI tools during development.

### Why AI SDLC in Angular?
- **Smart Development**: AI assistants (GitHub Copilot, Claude, Gemini)
- **AI-Powered Features**: LLMs, chatbots, intelligent automation
- **Better UX**: Dynamic, personalized experiences
- **Faster Development**: AI code generation, testing, debugging

---

## 2. AI SDLC Architecture Diagram

### High-Level Architecture

```
PLANNING → SETUP → BACKEND → FRONTEND → TESTING → DEPLOYMENT

User Input → Angular UI → API Call → Genkit Flow → LLM (Gemini) 
    ↑___________________________________________________________|
```

### Agentic SDLC Layers

```
PLANNING LAYER:
/grill-with-docs → /to-prd → /to-issues

BACKLOG LAYER:
Business Context + Acceptance Criteria + Technical Notes

BUILD LAYER:
/triage → /handoff → /tdd → /qa
```

### Detailed Phase Diagram

Phase 1: PLANNING (AI Requirements Analysis)
  - Define Epic with business context
  - Create PRD with AI assistance
  - Generate backlog tickets

Phase 2: SETUP (AI-Powered Development Environment)
  - Angular project setup
  - Genkit CLI installation
  - Gemini API configuration

Phase 3: BACKEND (Genkit Flows & Agents)
  - Define AI tools
  - Create flows
  - Configure LLM models

Phase 4: FRONTEND (Angular Components)
  - Chat UI with Signals
  - HTTP Client integration
  - Real-time streaming

Phase 5: TESTING (AI-Assisted Testing)
  - E2E tests with Agent Browser
  - AI QA verification
  - Stream testing

Phase 6: DEPLOYMENT (Cloud + AI)
  - Cloud Run deployment
  - Vertex AI integration
  - Monitoring & Observability

---

## 3. Phase-by-Phase Breakdown

### Phase 1: Planning with AI

**Tools Used:**
- `/grill-with-docs` - AI skill to define epic with business context
- `/to-prd` - Convert discussions to Product Requirements Document
- `/to-issues` - Generate backlog tickets from PRD

**Steps:**
1. **Define the Epic**: Use AI to ask strategic questions
   - Why does this feature matter?
   - Who are the users?
   - What's the success criteria?
   - What are we NOT building?

2. **Create PRD**: AI generates structured requirements document
   - Business Goal
   - User Stories
   - Success Criteria
   - Constraints

3. **Generate Backlog**: AI creates technical tasks from PRD
   - Setup Genkit flow
   - Create Angular chat component
   - Implement tool calling for order lookup

### Phase 2: Technical Setup

**Option A: Firebase AI Logic (Client-Side)**
```bash
npm install @genkit-ai @genkit-ai/next
```

**Option B: Genkit Full-Stack (Recommended)**
```bash
npm install -g genkit-cli
npm install @genkit-ai @genkit-ai/googleai
```

**Setup .env:**
```env
GOOGLE_GENAI_API_KEY=your_api_key
GOOGLE_CLOUD_PROJECT=your_project_id
```

### Phase 3: Backend Development with Genkit

#### Step 1: Define Tools
```typescript
// src/backend/tools/orderTools.ts
import { tool } from '@genkit-ai/core';
import { z } from 'zod';

export const getOrderStatus = tool(
  {
    description: 'Get the status of an order by order ID',
    inputSchema: z.object({
      orderId: z.string().describe('The order ID to look up'),
    }),
    outputSchema: z.object({
      orderId: z.string(),
      status: z.string(),
      estimatedDelivery: z.string(),
      items: z.array(z.string()),
    }),
  },
  async (input) => {
    // Mock database call
    return {
      orderId: input.orderId,
      status: 'Shipped',
      estimatedDelivery: '2025-01-20',
      items: ['Product A', 'Product B'],
    };
  }
);
```
#### Step 2: Create AI Flow
```typescript
// src/backend/flows/orderSupportFlow.ts
import { defineFlow } from '@genkit-ai/core';
import { googleAI } from '@genkit-ai/googleai';
import { z } from 'zod';
import { getOrderStatus } from '../tools/orderTools';

export const orderSupportFlow = defineFlow(
  {
    name: 'orderSupportFlow',
    inputSchema: z.object({ prompt: z.string() }),
    outputSchema: z.object({ response: z.string() }),
  },
  async (input) => {
    const llm = googleAI('gemini-2.0-flash');
    
    const response = await llm.generate({
      model: 'gemini-2.0-flash',
      prompt: input.prompt,
      tools: [getOrderStatus],
    });
    
    return { response: response.text };
  }
);
```

#### Step 3: Start Genkit Developer UI
```bash
npx genkit start -- tsx src/index.ts
# Opens at http://localhost:4001
```

### Phase 4: Frontend Development with Angular

#### Step 1: Create Angular Service
```typescript
// src/app/services/ai.service.ts
import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

@Injectable({
  providedIn: 'root'
})
export class AIService {
  private apiUrl = 'http://localhost:4001/api/orderSupportFlow';
  messages = signal<ChatMessage[]>([]);
  isLoading = signal<boolean>(false);

  constructor(private http: HttpClient) {}

  sendMessage(userMessage: string): Observable<string> {
    this.messages.update(msgs => [
      ...msgs,
      { role: 'user', content: userMessage, timestamp: new Date() }
    ]);
    
    this.isLoading.set(true);
    
    return this.http.post<{ response: string }>(this.apiUrl, {
      prompt: userMessage
    }).pipe(
      map(result => {
        this.messages.update(msgs => [
          ...msgs,
          { role: 'assistant', content: result.response, timestamp: new Date() }
        ]);
        this.isLoading.set(false);
        return result.response;
      }),
      catchError(err => {
        this.isLoading.set(false);
        throw err;
      })
    );
  }
}
```

---

## 4. Step-by-Step Examples

### Example 1: Simple Chatbot

#### Step 1: Setup
```bash
ng new ai-chatbot --standalone
cd ai-chatbot
npm install @genkit-ai @genkit-ai/googleai
```

#### Step 2: Create Genkit Flow
```typescript
// src/genkit/flows/chatFlow.ts
import { defineFlow } from '@genkit-ai/core';
import { googleAI } from '@genkit-ai/googleai';
import { z } from 'zod';

export const chatFlow = defineFlow(
  {
    name: 'chatFlow',
    inputSchema: z.object({ message: z.string() }),
    outputSchema: z.object({ reply: z.string() }),
  },
  async (input) => {
    const response = await googleAI('gemini-2.0-flash').generate({
      prompt: input.message,
    });
    return { reply: response.text };
  }
);
```

#### Step 3: Create Angular Service
```typescript
// src/app/services/chat.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class ChatService {
  constructor(private http: HttpClient) {}

  sendMessage(message: string): Observable<string> {
    return this.http.post<{ reply: string }>('/api/chatFlow', 
      { message }
    ).pipe(
      map(res => res.reply),
      catchError(err => {
        console.error('Chat error:', err);
        return ['Sorry, I encountered an error. Please try again.'];
      })
    );
  }
}
```

#### Step 4: Create Chat UI Component
```typescript
// src/app/components/simple-chat/simple-chat.component.ts
import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../services/chat.service';

@Component({
  selector: 'app-simple-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="chat">
      <div *ngFor="let msg of messages" [class]="msg.role">
        <strong>{{ msg.role === 'user' ? 'You' : 'AI' }}:</strong>
        {{ msg.content }}
      </div>
      <div class="input">
        <input [(ngModel)]="newMessage" (keydown.enter)="send()" placeholder="Type a message..." />
        <button (click)="send()">Send</button>
      </div>
    </div>
  `,
  styles: [
    `.chat { border: 1px solid #ccc; padding: 16px; border-radius: 8px; height: 400px; display: flex; flex-direction: column; }`,
    `.user { text-align: right; color: #007bff; }`,
    `.assistant { text-align: left; color: #333; }`,
    `.input { display: flex; gap: 8px; margin-top: auto; }`,
    `input { flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }`
  ]
})
export class SimpleChatComponent {
  private chatService = inject(ChatService);
  messages: { role: string; content: string }[] = [];
  newMessage = '';

  send() {
    if (!this.newMessage.trim()) return;
    
    this.messages.push({ role: 'user', content: this.newMessage });
    const userMsg = this.newMessage;
    this.newMessage = '';

    this.chatService.sendMessage(userMsg).subscribe(reply => {
      this.messages.push({ role: 'assistant', content: reply });
    });
  }
}
```
### Example 2: RAG (Retrieval Augmented Generation)

#### Step 1: Install Dependencies
```bash
npm install @genkit-ai/retriever
```

#### Step 2: Create Vector Store Retriever
```typescript
// src/genkit/retrievers/productRetriever.ts
import { defineRetriever } from '@genkit-ai/ai';
import { z } from 'zod';

export const productRetriever = defineRetriever(
  {
    name: 'productRetriever',
    configSchema: z.object({
      topK: z.number().default(5),
    }),
    metadataSchema: z.object({
      id: z.string(),
      name: z.string(),
      category: z.string(),
    }),
  },
  async (query, options) => {
    // Mock vector search - in production use Pinecone, Weaviate, etc.
    const products = await searchProducts(query.text, options?.topK);
    
    return {
      documents: products.map(p => ({
        content: `${p.name} - ${p.description}`,
        metadata: { id: p.id, name: p.name, category: p.category },
      })),
      totalTokens: products.length,
    };
  }
);
```

#### Step 3: Create RAG Flow
```typescript
// src/genkit/flows/productSearchFlow.ts
import { defineFlow } from '@genkit-ai/core';
import { googleAI } from '@genkit-ai/googleai';
import { productRetriever } from '../retrievers/productRetriever';
import { z } from 'zod';

export const productSearchFlow = defineFlow(
  {
    name: 'productSearchFlow',
    inputSchema: z.object({ query: z.string() }),
    outputSchema: z.object({ answer: z.string(), products: z.array(z.string()) }),
  },
  async (input) => {
    const response = await googleAI('gemini-2.0-flash').generate({
      prompt: `Answer the user's question based on the product catalog.
      Question: ${input.query}`,
      retrievers: [productRetriever],
    });

    return {
      answer: response.text,
      products: response.retrievals?.map(r => r.document.metadata.name) || [],
    };
  }
);
```
### Example 3: Multi-Agent System

```typescript
// src/genkit/agents/agentTeam.ts
import { defineAgent } from '@genkit-ai/core';
import { googleAI } from '@genkit-ai/googleai';
import { z } from 'zod';

// Agent 1: Customer Support
export const supportAgent = defineAgent({
  name: 'supportAgent',
  description: 'Handles customer inquiries and complaints',
  model: googleAI('gemini-2.0-flash'),
  tools: [getOrderStatus, initiateReturn],
});

// Agent 2: Sales Agent
export const salesAgent = defineAgent({
  name: 'salesAgent',
  description: 'Handles product recommendations and upsells',
  model: googleAI('gemini-2.0-flash'),
  tools: [searchProducts, applyDiscount],
});

// Orchestrator
export const orchestratorFlow = defineFlow(
  {
    name: 'orchestratorFlow',
    inputSchema: z.object({ message: z.string() }),
    outputSchema: z.object({ 
      response: z.string(),
      agentUsed: z.string()
    }),
  },
  async (input) => {
    // Classify intent
    const intent = await googleAI('gemini-2.0-flash').generate({
      prompt: `Classify this message as "support", "sales", or "general": ${input.message}`,
      output: { schema: z.object({ intent: z.enum(['support', 'sales', 'general']) }) },
    });

    // Route to appropriate agent
    let response;
    switch (intent.intent) {
      case 'support':
        response = await supportAgent.run(input.message);
        break;
      case 'sales':
        response = await salesAgent.run(input.message);
        break;
      default:
        response = await googleAI('gemini-2.0-flash').generate({
          prompt: input.message
        });
    }

    return { response: response.text, agentUsed: intent.intent };
  }
);
```

---

## 5. YouTube Videos & Resources

### Recommended YouTube Videos

1. **Building the future of apps with Angular and AI**
   - Link: https://www.youtube.com/watch?v=B6m_QD81CSo
   - Topics: Genkit setup, AI flows, tool calling, streaming

2. **Angular AI Agentic Apps Workshop**
   - Link: https://www.youtube.com/watch?v=Jm7wQa547qI
   - Topics: Building complete agentic apps with Genkit

3. **Building AI-Powered Angular Apps**
   - Link: https://www.youtube.com/watch?v=8lG98r8Brwc
   - Topics: Firebase AI Logic, Gemini API integration

### Essential Articles

1. **Angular Official AI Guide**
   - Link: https://angular.dev/ai
   - Complete documentation on AI integration

2. **Agentic SDLC by Lorenzo GM**
   - Link: https://lorenzogm.com/en/blog/agentic-software-development-life-cycle
   - Structured workflow for AI-assisted development

3. **Genkit + Angular by Avidclan**
   - Link: https://www.avidclan.com/blog/the-complete-guide-to-building-ai-powered-apps-with-genkit-and-angular/
   - Complete implementation guide

4. **Telerik Agentic Apps Tutorial**
   - Link: https://www.telerik.com/blogs/build-agentic-apps-angular-genkit-kendo-ui-part-2
   - Step-by-step with code examples

### GitHub Repositories

1. **Angular Story Generator (Official)**
   - Link: https://github.com/angular/examples/tree/main/genkit-angular-story-generator
   - Complete working example

2. **Agentic Order Support App**
   - Link: https://github.com/danywalls/agentic-app
   - Chat app with tool calling

### Interactive Tutorials

1. **Google Codelab: Deploy Angular + Vertex AI**
   - Link: https://codelabs.developers.google.com/codelabs/deploy-from-github/gen-ai-angular
   - Hands-on tutorial with Cloud Run deployment

---

## 6. Complete Working Example

### Project Structure
```
ai-angular-app/
├── backend/
│   ├── src/
│   │   ├── index.ts                 # Genkit entry point
│   │   ├── flows/
│   │   │   └── chatFlow.ts
│   │   ├── tools/
│   │   │   └── orderTools.ts
│   │   └── retrievers/
│   │       └── productRetriever.ts
│   ├── package.json
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── services/
│   │   │   │   └── ai.service.ts
│   │   │   ├── components/
│   │   │   │   └── chat/
│   │   │   │       └── chat.component.ts
│   │   │   ├── app.config.ts
│   │   │   └── app.component.ts
│   └── angular.json
├── docker-compose.yml
└── README.md
```

### Backend Implementation

```typescript
// backend/src/index.ts
import { genkit } from '@genkit-ai/core';
import { googleAI } from '@genkit-ai/googleai';
import { orderSupportFlow } from './flows/orderSupportFlow';
import { productSearchFlow } from './flows/productSearchFlow';

export const ai = genkit({
  plugins: [googleAI()],
  flows: [orderSupportFlow, productSearchFlow],
});

console.log('Genkit server running on http://localhost:4001');
```

### Frontend Implementation

```typescript
// frontend/src/app/app.component.ts
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ChatComponent } from './components/chat/chat.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, ChatComponent],
  template: `
    <div class="app">
      <header>
        <h1>AI-Powered Angular App</h1>
        <nav>
          <a href="#chat">Chat</a>
          <a href="#features">Features</a>
        </nav>
      </header>
      
      <main>
        <app-chat></app-chat>
      </main>
      
      <footer>
        <p>Built with Angular 22 + Genkit + Gemini AI</p>
      </footer>
    </div>
  `,
})
export class AppComponent {}
```

### Package.json Configuration

```json
{
  "name": "ai-angular-backend",
  "version": "1.0.0",
  "scripts": {
    "start": "genkit start -- tsx src/index.ts",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "@genkit-ai/core": "^1.0.0",
    "@genkit-ai/googleai": "^1.0.0",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "tsx": "^4.7.0",
    "typescript": "^5.3.0"
  }
}
```

---

## 7. Extra Features & Best Practices

### Feature 1: Streaming Responses

```typescript
// backend/src/flows/streamingChatFlow.ts
export const streamingChatFlow = defineFlow(
  { name: 'streamingChatFlow', ... },
  async (input) => {
    const stream = await googleAI('gemini-2.0-flash').stream({
      prompt: input.message,
    });
    
    let fullResponse = '';
    for await (const chunk of stream) {
      fullResponse += chunk.text;
    }
    
    return { reply: fullResponse };
  }
);
```

### Feature 2: Conversation History Management

```typescript
// services/conversation-history.service.ts
@Injectable({ providedIn: 'root' })
export class ConversationHistoryService {
  conversations = signal<Conversation[]>([]);
  currentConversation = signal<Conversation | null>(null);

  createNewConversation() {
    const newConversation: Conversation = {
      id: Date.now().toString(),
      title: 'New Chat',
      messages: [],
      createdAt: new Date(),
    };
    this.conversations.update(convs => [newConversation, ...convs]);
    this.currentConversation.set(newConversation);
  }
}
```

### Feature 3: AI Prompt Templates

```typescript
// services/prompt-templates.service.ts
interface PromptTemplate {
  name: string;
  systemPrompt: string;
  userPromptTemplate: string;
}

@Injectable({ providedIn: 'root' })
export class PromptTemplatesService {
  templates: PromptTemplate[] = [
    {
      name: 'Customer Support',
      systemPrompt: 'You are a helpful customer support agent.',
      userPromptTemplate: 'Customer asks: {{message}}. Order: {{orderContext}}',
    },
  ];

  buildPrompt(templateName: string, variables: Record<string, any>): string {
    const template = this.templates.find(t => t.name === templateName);
    let prompt = template!.userPromptTemplate;
    for (const [key, value] of Object.entries(variables)) {
      prompt = prompt.replace(`{{${key}}}`, value);
    }
    return `${template!.systemPrompt}\n\n${prompt}`;
  }
}
```

### Feature 4: Error Handling & Fallbacks

```typescript
// services/ai-error-handler.service.ts
@Injectable({ providedIn: 'root' })
export class AIErrorHandlerService {
  errors = signal<AIError[]>([]);
  fallbackMode = signal<boolean>(false);

  async executeWithFallback<T>(
    aiOperation: () => Promise<T>,
    fallbackOperation: () => Promise<T>
  ): Promise<T> {
    try {
      const result = await aiOperation();
      this.fallbackMode.set(false);
      return result;
    } catch (error) {
      this.errors.update(errs => [...errs, {
        timestamp: new Date(),
        error: error instanceof Error ? error.message : 'Unknown',
      }]);
      this.fallbackMode.set(true);
      return await fallbackOperation();
    }
  }
}
```

### Feature 5: Rate Limiting & Caching

```typescript
// middleware/aiRateLimiter.ts
import { Ratelimit } from '@upstash/ratelimit';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '1 m'),
});

export async function checkRateLimit(userId: string) {
  const { success } = await ratelimit.limit(userId);
  if (!success) throw new Error('Rate limit exceeded');
}

const aiCache = new Map<string, { response: any; timestamp: number }>();
export function getCachedResponse(promptHash: string) {
  const cached = aiCache.get(promptHash);
  if (cached && Date.now() - cached.timestamp < 3600000) {
    return cached.response;
  }
  return null;
}
```
### Feature 6: AI-Powered Code Generation

```typescript
// scripts/ai-generate-component.ts
async function generateComponent(description: string) {
  const prompt = `Generate an Angular standalone component for: ${description}
  Include TypeScript class, HTML template, and CSS styles.`;
  
  const response = await googleAI('gemini-2.0-flash').generate({
    prompt,
    output: { format: 'code' },
  });

  return response.text;
}
```

### Feature 7: Monitoring & Observability

```typescript
// observability/ai-monitoring.ts
import { trace } from '@opentelemetry/api';

export function monitorAIOperation<T>(
  operationName: string,
  operation: () => Promise<T>
): Promise<T> {
  const span = trace.getTracer('ai-service').startSpan(operationName);
  
  return span.traceAsync(() => {
    const startTime = Date.now();
    return operation()
      .then(result => {
        const duration = Date.now() - startTime;
        console.log(`[AI Monitor] ${operationName}: ${duration}ms`);
        span.end();
        return result;
      })
      .catch(error => {
        span.setAttributes({ 'ai.error': error.message });
        span.end();
        throw error;
      });
  });
}
```

### Best Practices Checklist

**Development Phase**
- [ ] Use type-safe schemas (Zod) for all AI inputs/outputs
- [ ] Implement comprehensive error handling
- [ ] Add loading states and user feedback
- [ ] Use environment variables for API keys
- [ ] Document all flows and tools

**Security**
- [ ] Never expose API keys in frontend code
- [ ] Implement rate limiting on AI endpoints
- [ ] Validate and sanitize all user inputs
- [ ] Use authentication for production deployments
- [ ] Monitor for prompt injection attacks

**Performance**
- [ ] Cache frequent AI responses
- [ ] Implement streaming for better UX
- [ ] Use connection pooling for database calls
- [ ] Optimize prompts to reduce token usage
- [ ] Monitor latency and set timeouts

**User Experience**
- [ ] Show loading indicators during AI processing
- [ ] Provide fallback responses on errors
- [ ] Allow users to regenerate responses
- [ ] Include feedback mechanism (thumbs up/down)
- [ ] Support conversation history

---

## Quick Reference Commands

```bash
# Setup Angular project
ng new ai-app --standalone
cd ai-app

# Install Genkit
npm install -g genkit-cli
npm install @genkit-ai/core @genkit-ai/googleai zod

# Start Genkit Developer UI
npx genkit start -- tsx src/index.ts

# Run Angular app
ng serve

# Deploy to Cloud Run
gcloud builds submit --tag gcr.io/$PROJECT_ID/angular-ai-app
gcloud run deploy angular-ai-app --image gcr.io/$PROJECT_ID/angular-ai-app

# View logs
gcloud logs read --project=$PROJECT_ID --filter="resource.type=cloud_run_revision"
```

---

## Summary

This guide covered:

1. **AI SDLC Architecture**: 6-phase workflow from planning to deployment
2. **Agentic SDLC**: Planning → Backlog → Build with AI skills
3. **Step-by-Step Examples**: Chatbot, RAG, Multi-agent systems
4. **Complete Code**: Working examples with Genkit + Angular
5. **Extra Features**: Streaming, caching, monitoring, error handling
6. **Resources**: YouTube videos, articles, GitHub repos

### Next Steps

1. Start with the official Angular AI guide: https://angular.dev/ai
2. Try the Google Codelab for hands-on practice
3. Experiment with the GitHub examples
4. Build your first chatbot using this guide
5. Explore advanced features like RAG and multi-agent systems

### Additional Learning Paths

- **Beginner**: Start with Firebase AI Logic (client-side only)
- **Intermediate**: Move to Genkit full-stack with tool calling
- **Advanced**: Implement multi-agent systems and RAG with vector databases
- **Expert**: Add observability, streaming, and production optimizations

---

## Questions & Support

- Angular Discord: https://discord.gg/angular
- Genkit Docs: https://firebase.google.com/docs/genkit
- GitHub Issues: https://github.com/angular/angular

---

**Last Updated**: January 2026
**Angular Version**: 22+
**Genkit Version**: 1.0+
