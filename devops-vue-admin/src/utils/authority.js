import { LocalStorage } from 'quasar';

// use localStorage to store the authority info, which might be sent from server in actual project.
export function getAuthority(str) {
  // return localStorage.getItem('devops-vue-admin-authority') || ['superuser', 'user'];
  const authorityString =
    typeof str === 'undefined'
      ? LocalStorage.getItem('devops-vue-admin-authority')
      : str;
  // authorityString could be admin, "admin", ["admin"]
  let authority;
  try {
    authority = JSON.parse(authorityString);
  } catch (e) {
    authority = authorityString;
  }
  if (typeof authority === 'string') {
    return [authority];
  }
  return authority || ['guest'];
}

export function setAuthority(authority) {
  const proAuthority = typeof authority === 'string' ? [authority] : authority;
  return LocalStorage.set('devops-vue-admin-authority', proAuthority);
}
