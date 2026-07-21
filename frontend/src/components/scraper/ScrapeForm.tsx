import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "../ui/card";
import { Button } from "../ui/button";
import { Input } from "../ui/input";

interface ScrapeFormProps {
  onStart: (keyword: string, targetCount: number) => void;
  disabled: boolean;
}

export function ScrapeForm({ onStart, disabled }: ScrapeFormProps) {
  const [keyword, setKeyword] = useState("");
  const [count, setCount] = useState("50");

  const handleSubmit = () => {
    if (keyword.trim()) {
      onStart(keyword.trim(), parseInt(count) || 50);
    }
  };

  return (
    <Card className="max-w-xl mx-auto">
      <CardHeader>
        <CardTitle>Scrape Nepali Tweets</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <label className="text-sm font-medium">Keyword</label>
          <Input 
            placeholder="e.g. नेपाल, सरकार, बाटो" 
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            disabled={disabled}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Target Count</label>
          <Input 
            type="number"
            min="10"
            max="200"
            value={count}
            onChange={(e) => setCount(e.target.value)}
            disabled={disabled}
          />
        </div>
      </CardContent>
      <CardFooter className="flex justify-end">
        <Button onClick={handleSubmit} disabled={disabled || !keyword.trim()}>
          Start Scraping
        </Button>
      </CardFooter>
    </Card>
  );
}
