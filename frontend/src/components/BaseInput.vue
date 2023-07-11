<template>
  <div class="form-group"
       :class="[
         {'input-group': hasIcon},
         {'has-danger': error},
         {'focused': focused},
         {'input-group-alternative': alternative},
         {'has-label': label || $slots.label},
         {'has-success': valid === true},
         {'has-danger': valid === false}
       ]">
    <slot name="label">
      <label v-if="label" :class="labelClasses">
        {{label}}
        <span v-if="required">*</span>
      </label>
    </slot>

    <div v-if="addonLeftIcon || $slots.addonLeft" class="input-group-prepend">
      <span class="input-group-text">
        <slot name="addonLeft">
          <i :class="addonLeftIcon"></i>
        </slot>
      </span>
    </div>

    <slot v-bind="slotData">
      <input
        v-model="internalValue"
        v-on="listeners"
        v-bind="$attrs"
        class="form-control"
        :class="[{'is-valid': valid === true}, {'is-invalid': valid === false}, inputClasses]"
        aria-describedby="addon-right addon-left"
      >
    </slot>

    <div v-if="addonRightIcon || $slots.addonRight" class="input-group-append">
      <span class="input-group-text">
        <slot name="addonRight">
          <i :class="addonRightIcon"></i>
        </slot>
      </span>
    </div>

    <slot name="infoBlock"></slot>

    <slot name="helpBlock">
      <div class="text-danger invalid-feedback" style="display: block;" :class="{'mt-2': hasIcon}" v-if="error">
        {{ error }}
      </div>
    </slot>
  </div>
</template>

<script>
export default {
  inheritAttrs: false,
  name: "base-input",
  props: {
    required: {
      type: Boolean,
      default: false,
      description: "Whether input is required (adds an asterisk *)"
    },
    valid: {
      type: Boolean,
      description: "Whether it is valid",
      default: undefined
    },
    alternative: {
      type: Boolean,
      description: "Whether input has an alternative layout"
    },
    label: {
      type: String,
      description: "Input label (text before input)"
    },
    error: {
      type: String,
      description: "Input error (below input)"
    },
    labelClasses: {
      type: String,
      description: "Input label CSS classes"
    },
    inputClasses: {
      type: String,
      description: "Input CSS classes"
    },
    value: {
      type: [String, Number],
      description: "Input value",
      default: ''
    },
    addonRightIcon: {
      type: String,
      description: "Addon right icon"
    },
    addonLeftIcon: {
      type: String,
      description: "Addon left icon"
    }
  },
  data() {
    return {
      focused: false,
      internalValue: this.value // 내부에서 사용할 value 변수
    };
  },
  computed: {
    listeners() {
      return {
        ...this.$listeners,
        input: this.updateValue,
        focus: this.onFocus,
        blur: this.onBlur
      };
    },
    slotData() {
      return {
        focused: this.focused,
        ...this.listeners
      };
    },
    hasIcon() {
      const { addonRight, addonLeft } = this.$slots;
      return (
        addonRight !== undefined ||
        addonLeft !== undefined ||
        this.addonRightIcon !== undefined ||
        this.addonLeftIcon !== undefined
      );
    }
  },
  methods: {
    updateValue(evt) {
      let value = evt.target.value;
      this.internalValue = value; // 내부 value 변수에 값 할당
      this.$emit("input", value); // 부모 컴포넌트로 값 전달
    },
    onFocus(value) {
      this.focused = true;
      this.$emit("focus", value);
    },
    onBlur(value) {
      this.focused = false;
      this.$emit("blur", value);
    }
  }
};
</script>

<style>
</style>
