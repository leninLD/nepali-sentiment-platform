import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "../ui/card";
import { Textarea } from "../ui/textarea";
import { Button } from "../ui/button";

interface TextInputCardProps {
  onAnalyze: (text: string) => void;
  loading: boolean;
}

export function TextInputCard({ onAnalyze, loading }: TextInputCardProps) {
  const [text, setText] = useState("");

  const handleSubmit = () => {
    if (text.trim().length > 0) {
      onAnalyze(text.trim());
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Nepali Text Sentiment</CardTitle>
      </CardHeader>
      <CardContent>
        <Textarea
          placeholder="Paste or type your Nepali text here..."
          className="min-h-[150px] resize-y"
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={loading}
        />
      </CardContent>
      <CardFooter className="flex justify-end">
        <Button 
          onClick={handleSubmit} 
          disabled={loading || text.trim().length === 0}
        >
          {loading ? "Analyzing..." : "Analyze"}
        </Button>
      </CardFooter>
    </Card>
  );
}
