import React from "react";
import { Button, Form, FormGroup, Input, Label } from "reactstrap";
import axios from "axios";
import { API_URL } from "../constants";

class NewQueryForm extends React.Component {
  state = {
    pk: 0,
    model: "",
    modelv: "",
    query_input: "",
    query_output: "",
  };

  componentDidMount() {
    if (this.props.query) {
      const { pk, model, modelv, query_input, query_output } = this.props.query;
      this.setState({ pk, model, modelv, query_input, query_output });
    }
  }

  onChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  };

  createQuery = e => {
    e.preventDefault();
    axios.post(API_URL, this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
  };

  editQuery = e => {
    e.preventDefault();
    axios.put(`${API_URL}${this.state.pk}/`, this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
  };

  defaultIfEmpty = value => {
    return value === "" ? "" : value;
  };

  render() {
    return (
      <Form onSubmit={this.props.query ? this.editQuery : this.createQuery}>
        <FormGroup>
          <Label for="model">Model:</Label>
          <Input
            type="text"
            name="model"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.model)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="modelv">Model Version:</Label>
          <Input
            type="text"
            name="modelv"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.modelv)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="query_input">Query Input:</Label>
          <Input
            type="textarea"
            name="query_input"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.query_input)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="query_output">Query Output:</Label>
          <Input
            type="textarea"
            name="query_output"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.query_output)}
          />
        </FormGroup>
        <Button>Send</Button>
      </Form>
    );
  }
}

export default NewQueryForm;
