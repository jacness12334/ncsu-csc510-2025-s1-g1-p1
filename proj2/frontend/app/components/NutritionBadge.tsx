

type Props = {
  n?: {
    calories: number;
    protein?: number;
    carbs?: number;
    fat?: number;
  };
};

export default function NutritionBadge({ n }: Props) {
  if (!n) return null;
  
  return (
    <div className="mt-2 inline-flex gap-2 text-xs text-gray-500">
      <span>{n.calories} cal</span>
      {n.protein && <span>{n.protein}g protein</span>}
      {n.carbs && <span>{n.carbs}g carbs</span>}
      {n.fat && <span>{n.fat}g fat</span>}
    </div>
  );
}
