import { LocalStorage } from 'quasar';

export function set(key) {
  return function(pagination) {
    LocalStorage.set(key, pagination);
  };
}

export function get(key) {
  return function() {
    return LocalStorage.getItem(key);
  };
}
