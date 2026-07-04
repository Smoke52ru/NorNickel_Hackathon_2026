export interface Mention {
  nodeId: string
  start: number
  end: number
  label?: string
}

export interface Document {
  doc_id: string
  title: string
  year: number
  lang?: string
  source_path?: string
  text: string
  mentions?: Mention[]
}
