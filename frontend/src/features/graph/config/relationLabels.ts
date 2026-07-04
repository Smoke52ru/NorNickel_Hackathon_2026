export const RELATION_LABELS: Record<string, string> = {
  uses_material: 'использует материал',
  operates_at_condition: 'идёт при условии',
  produces_output: 'даёт результат/эффект',
  described_in: 'описано в источнике',
  validated_by: 'подтверждено',
  contradicts: 'противоречит',
  expert_in: 'эксперт в области',
  part_of: 'часть чего-либо',
  related: 'связано с',
}

export function getRelationLabel(relation: string): string {
  return RELATION_LABELS[relation] ?? relation.replace(/_/g, ' ')
}
