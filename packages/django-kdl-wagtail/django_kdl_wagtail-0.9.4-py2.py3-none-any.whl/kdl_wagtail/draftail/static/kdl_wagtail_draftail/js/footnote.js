const Modifier = window.DraftJS.Modifier
const EditorState = window.DraftJS.EditorState
const AtomicBlockUtils = window.DraftJS.AtomicBlockUtils

class FootnoteSource extends React.Component {
  componentDidMount() {
    const { editorState, entityType, onComplete } = this.props

    const src = window.prompt('Footnote')

    if (src) {
      const content = editorState.getCurrentContent()
      const contentWithEntity = content.createEntity(
        entityType.type,
        'MUTABLE',
        { src }
      )
      const entityKey = contentWithEntity.getLastCreatedEntityKey()
      const nextState = AtomicBlockUtils.insertAtomicBlock(
        editorState,
        entityKey,
        ' '
      )

      onComplete(nextState)
    } else {
      onComplete(editorState)
    }
  }

  render() {
    return null
  }
}

const Footnote = (props) => {
  const { entityKey, contentState } = props
  const data = contentState.getEntity(entityKey).getData()

  return React.createElement('div', { className: 'footnote' }, data.src)
}

window.draftail.registerPlugin({
  type: 'FOOTNOTE',
  source: FootnoteSource,
  decorator: Footnote
})
