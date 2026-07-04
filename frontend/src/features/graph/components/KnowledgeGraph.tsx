import { useEffect, useMemo, useRef } from 'react'
import { Network } from 'vis-network'
import { DataSet } from 'vis-data'
import { Card, Empty, Spin, theme } from 'antd'
import type { GraphData } from '@/shared/types/ask'
import { NODE_COLORS, NODE_TYPE_LABELS } from '../config/nodeStyles'
import { EDGE_STYLES, EDGE_FLAG_LABELS } from '../config/edgeStyles'
import { getRelationLabel } from '../config/relationLabels'
import { BRIDGE_EDGE_COLOR, getClusterBorderColor } from '../config/clusterStyles'
import { detectClusters, isBridgeEdge } from '../utils/detectClusters'
import { layoutClusters } from '../utils/layoutClusters'
import styles from './KnowledgeGraph.module.css'

interface KnowledgeGraphProps {
  graph: GraphData | null
  loading?: boolean
  hasAsked?: boolean
  focusedNodeId?: string | null
  embedded?: boolean
  panelOpen?: boolean
}

export function KnowledgeGraph({
  graph,
  loading = false,
  hasAsked = false,
  focusedNodeId = null,
  embedded = false,
  panelOpen = true,
}: KnowledgeGraphProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const networkRef = useRef<Network | null>(null)
  const { token } = theme.useToken()

  const clusterResult = useMemo(
    () => (graph ? detectClusters(graph) : null),
    [graph],
  )

  useEffect(() => {
    if (!containerRef.current || !graph || graph.nodes.length === 0 || !clusterResult) {
      networkRef.current?.destroy()
      networkRef.current = null
      return
    }

    const positions = layoutClusters(graph, clusterResult)

    const groups = Object.fromEntries(
      clusterResult.clusters.map((cluster) => [
        `cluster_${cluster.id}`,
        { borderWidth: 3, color: { border: getClusterBorderColor(cluster.id) } },
      ]),
    )

    const nodes = new DataSet(
      graph.nodes.map((node) => {
        const pos = positions.get(node.id)
        const clusterId = clusterResult.nodeCluster.get(node.id) ?? 0
        const borderColor = getClusterBorderColor(clusterId)
        const fillColor = NODE_COLORS[node.type]
        return {
          id: node.id,
          label: node.label,
          group: `cluster_${clusterId}`,
          x: pos?.x,
          y: pos?.y,
          color: {
            background: fillColor,
            border: borderColor,
            highlight: { background: fillColor, border: '#000' },
          },
          font: { color: token.colorText, size: 12, strokeWidth: 0 },
          title: `${NODE_TYPE_LABELS[node.type]}: ${node.label}`,
        }
      }),
    )

    const edges = new DataSet(
      graph.edges.map((edge, i) => {
        const style = EDGE_STYLES[edge.flag]
        const isBridge = isBridgeEdge(edge, clusterResult.bridgeEdges)
        const color = isBridge ? BRIDGE_EDGE_COLOR : style.color
        return {
          id: `e${i}`,
          from: edge.from,
          to: edge.to,
          label: getRelationLabel(edge.label),
          color: { color, highlight: color },
          width: isBridge ? 1 : style.width,
          dashes: isBridge ? [4, 4] : style.dashes,
          font: {
            size: 10,
            align: 'middle' as const,
            color: token.colorTextSecondary,
            background: token.colorBgContainer,
            strokeWidth: 0,
          },
          title: `${getRelationLabel(edge.label)} (${EDGE_FLAG_LABELS[edge.flag]})`,
        }
      }),
    )

    networkRef.current?.destroy()

    networkRef.current = new Network(
      containerRef.current,
      { nodes, edges },
      {
        groups,
        physics: {
          enabled: true,
          barnesHut: {
            gravitationalConstant: -5000,
            springLength: 80,
            springConstant: 0.06,
            avoidOverlap: 0.5,
          },
          stabilization: { iterations: 200 },
        },
        interaction: {
          hover: true,
          tooltipDelay: 100,
          zoomView: true,
          dragView: true,
          dragNodes: true,
        },
        edges: {
          smooth: { enabled: true, type: 'continuous', roundness: 0.5 },
          arrows: { to: { enabled: true, scaleFactor: 0.5 } },
        },
        nodes: {
          shape: 'dot',
          size: 18,
          borderWidth: 2,
        },
      },
    )

    networkRef.current.once('stabilizationIterationsDone', () => {
      networkRef.current?.setOptions({ physics: { enabled: false } })
    })

    return () => {
      networkRef.current?.destroy()
      networkRef.current = null
    }
  }, [graph, clusterResult, token.colorText, token.colorTextSecondary, token.colorBgContainer])

  useEffect(() => {
    if (!networkRef.current || !focusedNodeId) return

    networkRef.current.selectNodes([focusedNodeId])
    networkRef.current.focus(focusedNodeId, {
      scale: 1.2,
      animation: { duration: 500, easingFunction: 'easeInOutQuad' },
    })
  }, [focusedNodeId, graph])

  useEffect(() => {
    const container = containerRef.current
    if (!container) return

    const observer = new ResizeObserver(() => {
      networkRef.current?.redraw()
    })

    observer.observe(container)
    return () => observer.disconnect()
  }, [graph])

  useEffect(() => {
    if (!panelOpen || !networkRef.current) return

    const timer = window.setTimeout(() => {
      networkRef.current?.redraw()
      networkRef.current?.fit({
        animation: { duration: 200, easingFunction: 'easeInOutQuad' },
      })
    }, 300)

    return () => window.clearTimeout(timer)
  }, [panelOpen, graph])

  const isEmpty = !graph || graph.nodes.length === 0
  const showGraphLoading = loading && hasAsked && !isEmpty

  const graphContent = (
    <div className={styles.graphContainer}>
      {!hasAsked && !loading && (
        <div className={styles.emptyState}>
          <Empty description="Граф появится после запроса" />
        </div>
      )}

      {hasAsked && !loading && isEmpty && (
        <div className={styles.emptyState}>
          <Empty description="Нет узлов для отображения" />
        </div>
      )}

      {hasAsked && !isEmpty && (
        <div className={styles.graphArea}>
          {showGraphLoading && (
            <div className={styles.graphLoading}>
              <Spin size="large" tip="Строим граф…" />
            </div>
          )}
          <div ref={containerRef} className={styles.graph} />
        </div>
      )}

      {!isEmpty && (
        <div className={styles.legend}>
          <div className={styles.legendSection}>
            <span className={styles.legendTitle}>Типы узлов:</span>
            {(Object.keys(NODE_COLORS) as Array<keyof typeof NODE_COLORS>).map(
              (type) => (
                <span key={type} className={styles.legendItem}>
                  <span
                    className={styles.legendDot}
                    style={{ background: NODE_COLORS[type] }}
                  />
                  {NODE_TYPE_LABELS[type]}
                </span>
              ),
            )}
          </div>
          <div className={styles.legendSection}>
            <span className={styles.legendTitle}>Связи:</span>
            {(Object.keys(EDGE_STYLES) as Array<keyof typeof EDGE_STYLES>).map(
              (flag) => (
                <span key={flag} className={styles.legendItem}>
                  <span
                    className={styles.legendLine}
                    style={{
                      background: EDGE_STYLES[flag].color,
                      borderStyle: EDGE_STYLES[flag].dashes ? 'dashed' : 'solid',
                    }}
                  />
                  {EDGE_FLAG_LABELS[flag]}
                </span>
              ),
            )}
          </div>
          {clusterResult && clusterResult.clusters.length > 0 && (
            <div className={styles.legendSection}>
              <span className={styles.legendTitle}>Кластеры:</span>
              {clusterResult.clusters.map((cluster) => (
                <span key={cluster.id} className={styles.legendItem}>
                  <span
                    className={styles.legendRing}
                    style={{ borderColor: getClusterBorderColor(cluster.id) }}
                  />
                  {cluster.name}
                </span>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )

  if (embedded) {
    return <div className={styles.embeddedRoot}>{graphContent}</div>
  }

  return (
    <Card title="Граф знаний" className={styles.card}>
      {graphContent}
    </Card>
  )
}
