for cfg in ./*.yaml; do
  echo "Validating config: ${cfg}"
  esphome "${cfg}" compile
done
