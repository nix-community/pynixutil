## Pynix - Utility functions for working with data from Nix in Python

### Examples

#### Base32 encoding/decoding
``` python
import pynix

input = "v5sv61sszx301i0x6xysaqzla09nksnd"
b = pynix.b32decode(input)
output = pynix.b32encode(b)
assert input == output
```

#### Derivation parsing
``` python
import pynix

# Returns a dict with the same shape as nix show-derivation uses
d = pynix.drvparse(open("/nix/store/33cbakl9bg880apzjyvwwgkwsn8zzpcb-hello-2.10.drv").read())
print(d)
```

Returns a structure like
```
Derivation(outputs={'out': DerivationOutput(path='/nix/store/9rg06p1rcpw3y9m1xpji39w43zj0sny6-hello-2.10', hash_algo=None, hash=None)}, input_drvs={'/nix/store/0bwic13piazaq033zz893fhd40pb6sj7-stdenv-linux.drv': ['out'], '/nix/store/b7xrdpwx9jljhw32knn844xyvcmfkbfk-bash-4.4-p23.drv': ['out'], '/nix/store/vsf383dfgky6bplikvbvixyshkdzd9hz-hello-2.10.tar.gz.drv': ['out']}, input_srcs=['/nix/store/9krlzvny65gdc8s7kpb6lkx8cd02c25b-default-builder.sh'], system='x86_64-linux', builder='/nix/store/x0dcb2rxlzf32g0ddfkqqz1sfcyx4yay-bash-4.4-p23/bin/bash', args=['-e', '/nix/store/9krlzvny65gdc8s7kpb6lkx8cd02c25b-default-builder.sh'], env={'buildInputs': '', 'builder': '/nix/store/x0dcb2rxlzf32g0ddfkqqz1sfcyx4yay-bash-4.4-p23/bin/bash', 'configureFlags': '', 'depsBuildBuild': '', 'depsBuildBuildPropagated': '', 'depsBuildTarget': '', 'depsBuildTargetPropagated': '', 'depsHostHost': '', 'depsHostHostPropagated': '', 'depsTargetTarget': '', 'depsTargetTargetPropagated': '', 'doCheck': '1', 'doInstallCheck': '', 'name': 'hello-2.10', 'nativeBuildInputs': '', 'out': '/nix/store/9rg06p1rcpw3y9m1xpji39w43zj0sny6-hello-2.10', 'outputs': 'out', 'patches': '', 'pname': 'hello', 'propagatedBuildInputs': '', 'propagatedNativeBuildInputs': '', 'src': '/nix/store/3x7dwzq014bblazs7kq20p9hyzz0qh8g-hello-2.10.tar.gz', 'stdenv': '/nix/store/qdf49mvm79r83n9c9s7pkmmjqwhrw8jv-stdenv-linux', 'strictDeps': '', 'system': 'x86_64-linux', 'version': '2.10'})
```
