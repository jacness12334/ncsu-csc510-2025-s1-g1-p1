// app/components/NutritionBadge.tsx
import type { NutritionInfo } from "@/lib/types";

export default function NutritionBadge({ n }: { n?: NutritionInfo }) {
  if (!n) return null;
  return (
    <div className="mt-2 grid grid-cols-3 gap-2 rounded-lg border p-2 text-[10px] text-gray-700">
      <div><b>Calories</b><div>{n.calories}</div></div>
      <div><b>Carbs</b><div>{n.carbs ?? 0} g</div></div>
      <div><b>Fat</b><div>{n.fat ?? 0} g</div></div>
      {n.servingSize && (
        <div className="col-span-3 text-[10px] text-gray-500 mt-1">Serving: {n.servingSize}</div>
      )}
    </div>
  );
}
