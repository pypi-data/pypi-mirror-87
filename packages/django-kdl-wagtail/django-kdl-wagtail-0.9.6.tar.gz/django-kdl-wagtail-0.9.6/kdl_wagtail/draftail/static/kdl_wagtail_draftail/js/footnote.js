const Modifier = window.DraftJS.Modifier
const EditorState = window.DraftJS.EditorState

class FootnoteSource extends React.Component {
  componentDidMount() {
    const { editorState, entityType, onComplete } = this.props

    const src = window.prompt('Footnote')

    if (src) {
      const content = editorState.getCurrentContent()
      const selection = editorState.getSelection()

      const contentWithEntity = content.createEntity(
        entityType.type,
        'IMMUTABLE',
        { footnote: src }
      )
      const entityKey = contentWithEntity.getLastCreatedEntityKey()
      const text = `✱`

      const newContent = Modifier.replaceText(
        content,
        selection,
        text,
        null,
        entityKey
      )
      const nextState = EditorState.push(
        editorState,
        newContent,
        'insert-characters'
      )

      onComplete(nextState)
    } else {
      onComplete(editorState)
    }
  }

  render() {
    const { footnote } = 'footnote'

    return (
      <Modal
        onRequestClose={this.onRequestClose}
        onAfterOpen={this.onAfterOpen}
        isOpen
        contentLabel="Document chooser"
      >
        <form className="DocumentSource" onSubmit={this.onConfirm}>
          <label className="form-field">
            <span className="form-field__label">Document URL</span>
            <input
              ref={(inputRef) => {
                this.inputRef = inputRef
              }}
              type="text"
              onChange={this.onChangeURL}
              value={url}
              placeholder="www.example.com"
            />
          </label>

          <button type="submit">Save</button>
        </form>
      </Modal>
    )
  }
}

const Footnote = (props) => {
  const { entityKey, contentState } = props
  const data = contentState.getEntity(entityKey).getData()

  return React.createElement(
    'span',
    { className: 'footnote', 'data-footnote': data.footnote },
    props.children
  )
}

window.draftail.registerPlugin({
  type: 'FOOTNOTE',
  source: FootnoteSource,
  decorator: Footnote
})
