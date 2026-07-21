import { PageTransition } from "../components/PageTransition";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";

interface InfoRowProps {
  label: string;
  value: React.ReactNode;
}

function InfoRow({ label, value }: InfoRowProps) {
  return (
    <div className="flex flex-col sm:flex-row sm:items-center py-3 border-b last:border-0 gap-1 sm:gap-4">
      <span className="text-sm font-medium text-slate-500 sm:w-40 shrink-0">{label}</span>
      <span className="text-sm text-slate-800">{value}</span>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-lg">{title}</CardTitle>
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  );
}

export default function About() {
  return (
    <PageTransition>
      <div className="min-h-[calc(100vh-4rem)] bg-slate-50/50 px-4 py-10 sm:px-8">
        <div className="max-w-3xl mx-auto space-y-8">
          {/* Hero */}
          <div className="space-y-3">
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight">About This Project</h1>
            <p className="text-muted-foreground text-base leading-relaxed">
              This platform performs real-time sentiment analysis on Nepali political tweets.
              It scrapes live Nepali-script tweets via Nitter (no Twitter API key required),
              and classifies each one using a fine-tuned XLM-RoBERTa transformer — a state-of-the-art
              multilingual language model.
            </p>
          </div>

          {/* Model Details */}
          <Section title="🤖 Model">
            <InfoRow label="Architecture" value="XLM-RoBERTa (XLM-R)" />
            <InfoRow label="Task" value="Sequence Classification (Sentiment)" />
            <InfoRow
              label="Output Classes"
              value={
                <span className="flex flex-wrap gap-2">
                  <Badge className="bg-green-500 hover:bg-green-600">Positive</Badge>
                  <Badge variant="secondary">Neutral</Badge>
                  <Badge variant="destructive">Negative</Badge>
                </span>
              }
            />
            <InfoRow label="Fine-tuned on" value="Nepali political tweet dataset (Devanagari script)" />
            <InfoRow label="Base model" value="FacebookAI/xlm-roberta-base (125M params)" />
            <InfoRow label="Inference" value="PyTorch · runs on CPU or CUDA · ~200–500 ms/tweet" />
          </Section>

          {/* Language Constraint */}
          <Section title="🇳🇵 Language Constraint">
            <p className="text-sm text-slate-600 leading-relaxed">
              Only tweets containing at least <strong>25% Devanagari characters</strong> (by letter count)
              are accepted for analysis. This hard filter is enforced both in the scraper (before prediction)
              and in the text cleaner (before tokenization). English-only or mixed-script tweets are rejected.
            </p>
          </Section>

          {/* Preprocessing */}
          <Section title="🧹 Text Preprocessing Pipeline">
            <ol className="text-sm text-slate-600 space-y-1.5 list-decimal list-inside leading-relaxed">
              <li>Strip emojis &amp; Unicode control characters (zero-width joiners, etc.)</li>
              <li>Remove URLs (http, https, t.co, www, common TLDs)</li>
              <li>Remove @mentions and #hashtags</li>
              <li>Lowercase &amp; remove noise characters (punctuation, symbols)</li>
              <li>
                Keep only <strong>Devanagari</strong> (U+0900–U+097F),{" "}
                <strong>Latin a–z</strong>, and <strong>digits 0–9</strong>
              </li>
              <li>Collapse whitespace</li>
            </ol>
          </Section>

          {/* Scraper */}
          <Section title="🌐 Data Collection">
            <InfoRow label="Method" value="Headless Chrome + Selenium → Nitter" />
            <InfoRow label="API key required?" value="No — Nitter instances are free to use" />
            <InfoRow
              label="Failover"
              value="8 public Nitter instances tried in order; scraper stops gracefully if all are down"
            />
            <InfoRow label="Dedup" value="Exact-text deduplication per scrape job" />
            <InfoRow label="Language filter" value="25% Devanagari threshold applied before prediction" />
          </Section>

          {/* Architecture */}
          <Section title="🏗️ System Architecture">
            <div className="text-sm text-slate-600 space-y-2 leading-relaxed">
              <p>
                <strong>Backend:</strong> FastAPI (Python) with Uvicorn. Scrape jobs run as
                FastAPI <code className="bg-slate-100 px-1 rounded">BackgroundTasks</code> so the
                UI never blocks. Model is loaded once at startup via the FastAPI{" "}
                <code className="bg-slate-100 px-1 rounded">lifespan</code> event and held in
                <code className="bg-slate-100 px-1 rounded">app.state</code>.
              </p>
              <p>
                <strong>Frontend:</strong> React + Vite (TypeScript). Polls job status every 1.5 s.
                Charts via Recharts. Animations via Framer Motion. UI components from shadcn/ui +
                Tailwind CSS.
              </p>
              <p>
                <strong>Word Clouds:</strong> Generated server-side with the{" "}
                <code className="bg-slate-100 px-1 rounded">wordcloud</code> Python library using
                the Noto Sans Devanagari variable font, filtered by a custom Nepali stopword list.
                Served as PNG streams — no temp files written to disk.
              </p>
            </div>
          </Section>
        </div>
      </div>
    </PageTransition>
  );
}
