import type { AnalyzeResponse } from "../../hooks/useAnalyzeText";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "../ui/card";
import { Badge } from "../ui/badge";
import { Progress } from "../ui/progress";
import { motion } from "framer-motion";

interface PredictionResultProps {
  result: AnalyzeResponse;
}

export function PredictionResult({ result }: PredictionResultProps) {
  const { label, confidence_scores, response_time_ms } = result;

  // Determine colors based on label
  let badgeVariant: "default" | "secondary" | "destructive" | "outline" = "default";
  let badgeColorClass = "";
  
  if (label.toLowerCase() === "positive") {
    badgeColorClass = "bg-green-500 hover:bg-green-600";
  } else if (label.toLowerCase() === "negative") {
    badgeVariant = "destructive";
  } else {
    badgeVariant = "secondary";
  }

  // Pre-sort labels to keep the order consistent: Positive, Neutral, Negative
  const order = ["Positive", "Neutral", "Negative"];
  const sortedScores = Object.entries(confidence_scores).sort(
    (a, b) => order.indexOf(a[0]) - order.indexOf(b[0])
  );

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-2xl mx-auto mt-6"
    >
      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-xl font-bold">Analysis Result</CardTitle>
          <Badge variant={badgeVariant} className={`${badgeColorClass} px-3 py-1 text-sm`}>
            {label.toUpperCase()}
          </Badge>
        </CardHeader>
        <CardContent className="pt-4">
          <h4 className="text-sm font-semibold mb-3 text-muted-foreground">Confidence Scores</h4>
          <div className="space-y-4">
            {sortedScores.map(([cls, score]) => {
              const percentage = Math.round(score * 100);
              let colorClass = "bg-primary";
              if (cls.toLowerCase() === "positive") colorClass = "[&>div]:bg-green-500";
              if (cls.toLowerCase() === "negative") colorClass = "[&>div]:bg-red-500";
              if (cls.toLowerCase() === "neutral") colorClass = "[&>div]:bg-slate-400";

              return (
                <div key={cls} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium">{cls}</span>
                    <span>{percentage}%</span>
                  </div>
                  <Progress value={percentage} className={`h-2 ${colorClass}`} />
                </div>
              );
            })}
          </div>
        </CardContent>
        <CardFooter className="pt-2 text-xs text-muted-foreground justify-end">
          Response Time: {response_time_ms.toFixed(2)} ms
        </CardFooter>
      </Card>
    </motion.div>
  );
}
