import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { KnowledgeService } from '../../core/services/knowledge.service';
import { Citation } from '../../core/models/models';

interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  text: string;
  citations?: Citation[];
}

@Component({
  selector: 'app-assistant',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <h1>Assistant</h1>
    <p class="muted">Ask questions across your sprint documentation. Answers cite their sources.</p>

    <div class="chat">
      <div *ngIf="messages.length === 0" class="empty muted">
        Try: “Which sprint introduced prepaid variants?”
      </div>
      <div *ngFor="let m of messages" class="msg" [ngClass]="m.role">
        <div class="bubble">
          <div class="text">{{ m.text }}</div>
          <ul *ngIf="m.citations?.length" class="citations">
            <li *ngFor="let c of m.citations">
              {{ c.application || 'doc' }}<span *ngIf="c.sprint"> · {{ c.sprint }}</span><span *ngIf="c.page"> · p.{{ c.page }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <form class="composer" (ngSubmit)="send()">
      <input
        type="text"
        [(ngModel)]="draft"
        name="draft"
        placeholder="Ask a question…"
        [disabled]="busy"
        autocomplete="off"
      />
      <button type="submit" [disabled]="!draft.trim() || busy">{{ busy ? '…' : 'Send' }}</button>
    </form>
  `,
  styles: [
    `
      h1 { margin-top: 0; margin-bottom: 4px; }
      .muted { color: var(--muted); }
      .chat {
        background: var(--panel); border: 1px solid var(--border); border-radius: 10px;
        padding: 16px; min-height: 320px; display: flex; flex-direction: column; gap: 12px; margin: 16px 0;
      }
      .empty { text-align: center; margin: auto; }
      .msg { display: flex; }
      .msg.user { justify-content: flex-end; }
      .bubble { max-width: 78%; padding: 10px 14px; border-radius: 12px; font-size: 14px; line-height: 1.45; }
      .msg.user .bubble { background: var(--primary); color: #fff; border-bottom-right-radius: 4px; }
      .msg.assistant .bubble { background: #eef1f6; border-bottom-left-radius: 4px; }
      .msg.system .bubble { background: #fff4e5; color: #7a4b00; border: 1px solid #ffd8a8; }
      .citations { margin: 8px 0 0; padding-left: 16px; font-size: 12px; color: var(--muted); }
      .composer { display: flex; gap: 8px; }
      .composer input { flex: 1; font: inherit; padding: 10px 12px; border: 1px solid var(--border); border-radius: 8px; }
      .composer button { background: var(--primary); color: #fff; border-color: var(--primary); padding: 10px 18px; }
    `,
  ],
})
export class AssistantComponent {
  messages: ChatMessage[] = [];
  draft = '';
  busy = false;

  constructor(private knowledge: KnowledgeService) {}

  send(): void {
    const question = this.draft.trim();
    if (!question || this.busy) return;
    this.messages.push({ role: 'user', text: question });
    this.draft = '';
    this.busy = true;
    this.knowledge.ask(question).subscribe({
      next: (r) => {
        this.messages.push({ role: 'assistant', text: r.answer, citations: r.citations });
        this.busy = false;
      },
      error: () => {
        this.messages.push({
          role: 'system',
          text: 'Assistant unavailable — Knowledge-Service is not running yet.',
        });
        this.busy = false;
      },
    });
  }
}
