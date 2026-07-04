import { Button, Input, Space, Tag } from 'antd'
import styles from './QuestionForm.module.css'

const { TextArea } = Input

const EXAMPLE_QUESTIONS = [
  'Какие методы обессоливания воды подходят при сульфатах 200–300 мг/л?',
  'Какие решения циркуляции католита при электроэкстракции никеля описаны в мировой практике?',
  'Покажите эксперименты по распределению Au, Ag и МПГ между штейном и шлаком за последние 5 лет',
]

interface QuestionFormProps {
  value: string
  onChange: (value: string) => void
  onSubmit: () => void
  loading?: boolean
}

export function QuestionForm({
  value,
  onChange,
  onSubmit,
  loading = false,
}: QuestionFormProps) {
  const handleExampleClick = (q: string) => {
    onChange(q)
  }

  return (
    <div className={styles.form}>
      <Space.Compact style={{ width: '100%' }} size="large">
        <TextArea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Задайте вопрос на естественном языке…"
          autoSize={{ minRows: 2, maxRows: 4 }}
          onPressEnter={(e) => {
            if (!e.shiftKey) {
              e.preventDefault()
              if (value.trim() && !loading) onSubmit()
            }
          }}
          disabled={loading}
        />
        <Button
          type="primary"
          size="large"
          onClick={onSubmit}
          loading={loading}
          disabled={!value.trim()}
          className={styles.submitBtn}
        >
          Спросить
        </Button>
      </Space.Compact>
      <div className={styles.examples}>
        <span className={styles.examplesLabel}>Примеры:</span>
        {EXAMPLE_QUESTIONS.map((q) => (
          <Tag
            key={q}
            className={styles.exampleTag}
            onClick={() => handleExampleClick(q)}
            style={{ cursor: 'pointer' }}
          >
            {q.length > 60 ? `${q.slice(0, 60)}…` : q}
          </Tag>
        ))}
      </div>
    </div>
  )
}
